# str libraries
from typing import (
    Tuple,
    ClassVar,
    Union,
    Dict,
    List,
    NoReturn,
    Callable,
    Any
)
from argparse import Namespace
from time import sleep
from signal import signal, SIGINT, SIG_IGN

# third-party libraries
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.clipboard import Clipboard
from pyperclip import copy

# test
from rich.progress import track
# from prompt_toolkit.key_binding.bindings.named_commands import clear_screen

# own libraries
from modules.DataManagement import DataManagement
from modules.Visuals import Visuals
from modules.CreateSecurePassword import CreateSecurePasswords # change
from modules.Crypt import Hasher, PassCrypt
from utils.prompt_config import (
    set_tmp_kb,
    set_csp_kb,
    set_completer,
    welcome_msg
)

class StartCSP:
    """
    The StartCSP class serves as the enry point for the CSP tool. It handles
    user authenticatio and provides methods for initialising the tool and
    managing data.
    
    Attributes:
        AUTH_QUESTION (ClassVar[List[Tuple[str, str]]]): Representing the 
        autentication question presented to the user, with the format for
        required to 'message' from PromptSession class.
        _authenticated (bool): a flag indicating whether the user has been
        successfull authenticated.
    """
    AUTH_QUESTION: ClassVar[List[Tuple[str, str]]] = [
        ('class:msg', '[^] Enter the masterkey: ')
    ]
    _authenticated: ClassVar[bool] = False
    _passcrypt: ClassVar[Any]

    def __init__(self) -> None:
        self.vs: Visuals = Visuals()
        self.data_mgmt: DataManagement = DataManagement()
        self.tmp_session: PromptSession = PromptSession(
            message=StartCSP.AUTH_QUESTION,
            style=Style.from_dict({'msg': '#00b44e'}),
            is_password=True,
            key_bindings=set_tmp_kb()
        )
        if not StartCSP._authenticated:
            self.vs.banner()
            self.check_masterkey()

    def check_masterkey(self) -> NoReturn:
        """
        Check if the masterkey exits and realize the user authentication for
        start the tool. In case if all checkers are correct, change the value
        of StartCSP._authenticated to True
        """
        if not self.data_mgmt.masterkey_exists():
            self.create_and_store_masterkey()
        if not self._check_credentials():
            self._exit_csp()
        StartCSP._authenticated = True
        
    def create_and_store_masterkey(self, reset: bool=False) -> Union[None, str]:
        """
        Sets the master key for the first time usage or reset the exists masterkey.
        This method prompts the user to provide a masterkey. The user will be asked
        to type the master key twice to verify it.

        Args:
            reset (bool): If result its True execute sql sintax to update field in
            the database.
        
        Returns:
            None: when the reset arg its False.
            str: when the reset arg its True return the new masterkey.
        """
        if not reset:
            welcome_msg()
        while True:
            try:
                masterkey0: str = self.tmp_session.prompt()
                if masterkey0 != self.tmp_session.prompt():
                    self.vs.print(
                        'Password must be the same',
                        type='err',
                        end='\n'
                    )
                    continue
                if not CreateSecurePasswords.is_strong_password(masterkey0):
                    self.vs.print(
                        'The password does not meet the requirements',
                        type='err',
                        end='\n'
                    )
                    continue
                break
            except KeyboardInterrupt: self._exit_csp()
            except EOFError: self._exit_csp()
        if reset:
            self.data_mgmt.re_or_set_masterkey(masterkey0, mode='reset')
            return masterkey0
        self.data_mgmt.re_or_set_masterkey(masterkey0)
        self.vs.print('Masterkey inserted correctly', type='inf', end='\n')
    
    def _check_credentials(self, masterkey: str = None) -> bool:
        """
        Verifies the user's credentials. This method prompts the user to enter
        a masterkey and verifies if it is correct. The user has a maximum of 3
        attempts to enter the correct password. And set the _passcrypt with the
        introduce masterkey to cypher the data in future operations.

        Returns:
            bool: True if the credentials are correct, False if the attempts 
            are exceeded.
        """
        attempts: int = 3
        while attempts > 0:
            try:
                self.vs.print('Login CSP', type='inf')
                masterkey: str = self.tmp_session.prompt()
                if not self.data_mgmt.check_master_key(masterkey):
                    attempts -= 1
                    self.vs.print(
                        f'Incorrect masterkey. Attempts remaining: {attempts}',
                        type='err',
                        end='\n',
                        bad_render=True
                    )
                    continue
                StartCSP._passcrypt = PassCrypt(masterkey)
                del masterkey
                return True
            except KeyboardInterrupt as ki:
                self._exit_csp() if str(ki) == 'ControlD' else print(); continue
        self.vs.print(f'It has exceeded attempts', type='err')
        return False
    
    def _change_masterkey(self) -> Union[None, bool]:
        signal(SIGINT, SIG_IGN)
        self.vs.print(
            'Executing the masterkey change process..',
            type='inf',
            bad_render=True
        )
        self.vs.print(
            'Enter the actual masterkey to decryption of existing data.',
            type='inf',
        )
        old_masterkey: str = self.tmp_session.prompt()
        if not self.data_mgmt.check_master_key(old_masterkey):
            self.vs.print( 'The masterkey its invalid', type='err')
            return None
        old_crypt_raw_data = self.data_mgmt.list_data()
        old_raw_data = self._decrypt_listed_data(old_crypt_raw_data)
        
        self.vs.print(
            'Starting the process to create a new masterkey',
            type='inf',
            start='\n'
        )
        new_masterkey = self.create_and_store_masterkey(reset=True)
        StartCSP._passcrypt = PassCrypt(new_masterkey)
        self.vs.print(
            'Masterkey was created and stored succesfully',
            type='inf'
        )
        self.vs.print(
            'Beggining the process to encrypt the existing passwords',
            type='inf'
        )
        self.vs.print(
            f'Numbers of entries detected: {len(old_raw_data)}',
            type='inf',
            bad_render=True
        )
        for entry in track(old_raw_data, description='[bold blue]Encrypting[/bold blue]'):
            new_data: List[Union[str, int]] = [
                'password',
                entry[3],
                entry[0]
            ]
            self._update(new_data, skip_msg=True)
            sleep(0.10)

    def detect_mode( self, args: Namespace) -> Union['PromptCSP', 'OneLinerCSP']:
        """
        Detects the mode specified in the arguments and returns an instance
        of the corresponding class.

        Args:
            args (Namespace): The arguments passed to the method.

        Returns:
            Union[PromptCSP, InteractiveCSP, OneLinerCSP]: An instance of the
            class corresponding to the detected mode.
        """
        match args.mode:
            case 'prompt': return PromptCSP()
            case 'oneliner': return OneLinerCSP(args)

    def _list(self, args: List[str]) -> None:
        """
        Detect if the user wants to list the entire database or if he wants
        to make a specific query. The result render is rendered with method:
        'render_table_db()' of the Visual class
        
        Args:
            args (List[str]): If provided, the firts argument is the field to
            search and the second argument is the specific data to find.

        Return:
            None: Displays the queried data.
        """
        if len(args) != 0:
            raw_data = self._list_specific(args[:2])
            return None
        crypt_raw_data: List[Tuple[Union[int, str]]] = self.data_mgmt.list_data()
        raw_data: List[str] = self._decrypt_listed_data(crypt_raw_data)
        self.vs.render_table_db(raw_data)

    def _list_specific(self, args: List[str]) -> None:
        """
        List specific data from database based on the given field and data to
        find, this method its only called if _list() detect the user want a 
        custom query, The result render is rendered with method: 'render_table_db()'
        of the Visuals class but if data not exists or not found print a error
        message and end the method.

        Args:
            args (List[str]): If provided, the firts argument is the field to
            search and the second argument is the specific data to find.
        
        Return:
            None: Displays the queried data.
        """
        try: 
            field, data_to_find = args 
        except ValueError as ve: 
            self.vs.print(
                f'The atributes specify are wrong -> {ve}',
                type='err',
                bad_render=True
            )
            self.vs.print(
                'Try: [CSP> help] to see the help menu',
                type='war'
            )
            return None
                    
        crypt_raw_data: List[Tuple[Union[int, str]]] = self.data_mgmt.list_data(
            field,
            data_to_find
        )
        raw_data = self._decrypt_listed_data(crypt_raw_data)
        if len(raw_data) == 0:
            self.vs.print(
                'The requested value was not found in the database',
                type='err'
            )
            return None
        self.vs.render_table_db(raw_data)

    def _add(self, args: List[str]) -> None:
        """
        Create a new entry to database
        
        Args:
            args (List[str]): The argument depend on the data to be added. If
            adding a site, username, and password the list shoud contain three
            elements in that order.

        Retuns:
            None. Prints a message indicating whether the data was added 
            successfully
        """
        if len(args) == 3:
            site, username, password = args
        elif len(args) == 2:
            username, password = args
        else:
            password = args[0]
        crypt_raw_pass: Tuple[str] = StartCSP._passcrypt.encrypt(password)
        password = f'{crypt_raw_pass[0]}|{crypt_raw_pass[1]}|{crypt_raw_pass[2]}'
        if self.data_mgmt.new_entry(password, site, username):
            self.vs.print(
                f'Data inserted correcly', 
                type='inf'
            )

    def _delete(self, args: List[str]) -> None:
        """
        Delete data from the database based on the provided id. If the provided
        id not exists end the method, printing a error message.

        Args:
            args (List[str]): Content the id of the data to be deleted.

        Return:
            None: print a message if exec was success or not.
        """
        for id in args:
            if not self._check_exists_id(id):
                return None
            if self.data_mgmt.delete_data(id):
                self.vs.print(
                    'Data Deleted Correctly',
                    type='inf'
                )

    def _update(self, args: List[str], skip_msg: bool=False) -> None:
        """
        Update data in the database based ont he privided field, new data
        and id.

        Args:
            args (List[str]): Containing the field to update and the id.
                args[0]: The field to update.
                args[1]: The new data to replace the existing data.
                args[2]: The id of the data to be updated.
        
        Return:
            None: This method does not return any type.
        """
        try:
            field, data_upd, id = args
        except ValueError as ve: 
            self.vs.print(
                f'The atributes specify are wrong -> {ve}',
                type='err',
                bad_render=True
            )
            self.vs.print(
                'Try: [CSP> help] to see the help menu',
                type='war'
            )
            return None
        if not self._check_exists_id(id):
            return None
        if field == 'password':
            crypt_data_upd: Tuple[str] = StartCSP._passcrypt.encrypt(data_upd)
            data_upd: str = f'{crypt_data_upd[0]}|{crypt_data_upd[1]}|{crypt_data_upd[2]}'
        if self.data_mgmt.update_data(field, data_upd, id) and not skip_msg:
            self.vs.print( 'Data Updated Correctly', type='inf')

    def _reforcepass(self, args: List[str]) -> None:
        """
        Reinforces a given password by generating a stronger password using
        CreateSecurePasswords class.

        Args:
            args (List[str]): List containing the original password and a
            separator.

        Returns:
            None: This method does not return any value.
        """
        if len(args) > 2:
            #*password, separator = args
            password = args
            separator = ' '
            password: str = separator.join(password)
        else:
            password: str = args[0]
            separator: str = args[1]
        csp: CreateSecurePasswords = CreateSecurePasswords(
            password=password,
            separator=separator
        )
        reforce_pass: str = csp.create_strong_pass()
        self.vs.print('Password reforce succesfull', type='inf')
        if not csp.is_strong_password(reforce_pass):
            msg0: str = 'The generated password does not meet security '
            msg1: str = 'requirements. Use it at your own risk'
            self.vs.print(f'{msg0}{msg1}', type='war')
        self.vs.print(
            f'{reforce_pass} -> copied to clipboard',
            type='proc',
            bad_render=True
        )
        copy(reforce_pass)

    # posibly decorator in a future
    def _check_exists_id(self, id: str) -> bool:
        """
        Check if data with the provided ID exists in the database. If not
        exits print a error message.

        Args:
            id (str): The id to check for existence in database.
        
        Return:
            bool: True if data with the provided id exists, False otherwise
        """
        id_data = self.data_mgmt.list_data('id', id)
        if len(id_data) != 0:
            return True
        self.vs.print(
            f'The id: {id} does not exist, therefore the action cannot be executed',
            type='err',
            bad_render=True
        )
        return False

    def _exit_csp(self) -> NoReturn:
        """
        Exit the CSP tool. This method prints an exit message, saves an 
        necessary data, and terminates the program

        Return:
            NoReturn: end the program.
        """
        self.vs.print('Save and closing connection to database', type='inf')
        self.data_mgmt.save_and_exit(True)
        self.vs.print('Exiting..', type='err', bad_render=True)
        exit(0)
    
    def _proc_instruction(
        self,
        instruction: Union[str, bool]
    ) -> Union[Tuple[str, List[str]], List[str]]:
        # Proc true options ('change masterkey')
        if type(instruction).__name__ == 'bool':
            return instruction
        
        son_class: str = type(self).__name__
        if son_class == 'PromptCSP':
            command, *args = instruction.strip().split(' ')
            args = list(filter(lambda arg: arg != '', args))
            return (command, args)

        if son_class == 'OneLinerCSP':
            args = [
                word for proc_args in instruction
                for word in proc_args.strip().split(' ')
            ]
            args = list(filter(lambda arg: arg != '', args))
            return args

    def _decrypt_listed_data(self, crypt_raw_data) -> List[str]:
        decrypted_passwords = [
            StartCSP._passcrypt.decrypt(tuple(fields[3].split('|')))
            for fields in crypt_raw_data
        ]
        return [
            list(fields[:3]) + [password]
            for fields, password in zip(crypt_raw_data, decrypted_passwords)
        ]

class PromptCSP(StartCSP):
    def __init__(self) -> None:
        super().__init__()
        self.csp_session: PromptSession = PromptSession(
            message=[('class:prompt', '\nCSP> ')],
            style=Style.from_dict({'prompt': '#227547 bold'}),
            completer=set_completer(),
            complete_style=CompleteStyle.READLINE_LIKE,
            cursor=CursorShape.BEAM,
            key_bindings=set_csp_kb(),
        )

    def start_mode(self) -> None:
        while True:
            try:
                instruction: str = self.csp_session.prompt()
                self._check_command(instruction)
            except KeyboardInterrupt:
                self._check_command('^C')

    def _check_command(self, instruction: str) -> None:
        command, args = self._proc_instruction(instruction)
        match command:
            case 'list':
                self._list(args)
            case 'add':
                self._add(args)
            case 'del':
                self._delete(args)
            case 'upd':
                self._update(args)
            case 'reforcepass':
                self._reforcepass(args)
            case 'changemasterkey':
                self._change_masterkey()
            case 'help':
                self._help(args)
            case 'exit':
                self._exit_csp()
            case '^C':
                pass
            case _:
                self.vs.print('Command Not Fount: try [CSP> help]', type='err')

    def _help(self, args: List[str]):
        # in future
        pass
    
class OneLinerCSP(StartCSP):
    def __init__(self, args: Namespace) -> None:
        super().__init__()
        print()
        self.args = args
    
    def start_mode(self):
        for argument, args in self.args.__dict__.items():
            #print(f'{argument} -> {args} -> {type(args)}')
            if args is None: continue
            proc_args: Union[List[str], bool] = self._proc_instruction(args)
            match argument:
                case 'change_masterkey': 
                    if not proc_args: continue
                    self._change_masterkey()

                case 'execute':
                    tmp_prompt: PromptCSP = PromptCSP()
                    tmp_prompt._check_command(self.args.execute)

                case 'add': self._add(proc_args)
                case 'update': self._update(proc_args)
                case 'delete': self._delete(proc_args)
                case 'list': self._list(proc_args)
