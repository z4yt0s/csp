# str libraries
from typing import (
    Tuple,
    ClassVar,
    Union,
    Dict,
    List,
    NoReturn, 
)
from argparse import Namespace

# third-party libraries
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.clipboard import Clipboard
from pyperclip import copy
# from prompt_toolkit.key_binding.bindings.named_commands import clear_screen

# own libraries
from modules.DataManagement import DataManagement
from modules.Visuals import Visuals
from modules.CreateSecurePassword import CreateSecurePasswords # change
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
    _authenticated = False

    def __init__(self) -> None:
        self.vs: Visuals = Visuals()
        self.data_mgmt: DataManagement = DataManagement()
        if not StartCSP._authenticated:
            self.vs.banner()
            self.tmp_session: PromptSession = PromptSession(
                message=StartCSP.AUTH_QUESTION,
                style=Style.from_dict({'msg': '#00b44e'}),
                is_password=True,
                key_bindings=set_tmp_kb()
            )
            self.check_masterkey()

    def check_masterkey(self) -> NoReturn:
        """
        Check if the masterkey exits and realize the user authentication for
        start the tool. In case if all checkers are correct, change the value
        of StartCSP._authenticated to True
        """
        if not self.data_mgmt.masterkey_exists():
            self._set_masterkey()
        if not self._check_credentials():
            self._exit_csp()
        StartCSP._authenticated = True
        
    def _set_masterkey(self) -> None:
        """
        Sets the master key for the first time usage. This method prompts the
        user to provide a master key for the first time the CSP is run. The
        user will be asked to type the master key twice to verify it.
        """
        welcome_msg()
        while True:
            try:
                masterkey0: str = self.tmp_session.prompt()
                if masterkey0 != self.tmp_session.prompt():
                    self.vs.print('Password must be the same', type='err')
                    print()
                    continue
                if not CreateSecurePasswords.is_strong_password(masterkey0):
                    self.vs.print(
                        'The password does not meet the requirements',
                        type='err'
                    )
                    print()
                    continue
                break
            except KeyboardInterrupt: self._exit_csp()
            except EOFError: self._exit_csp()
        query: str = self.data_mgmt.predefined_sql('set_masterkey')
        self.data_mgmt.cursor.execute(query, (masterkey0,))
        self.vs.print('Masterkey inserted correctly', type='inf', end='\n')
    
    def _check_credentials(self):
        """
        Verifies the user's credentials. This method prompts the user to enter
        a masterkey and verifies if it is correct. The user has a maximum of 3
        attempts to enter the correct password.

        Returns:
            bool: True if the credentials are correct, False if the attempts 
            are exceeded.
        """
        attempts: int = 3
        while attempts > 0:
            try:
                self.vs.print('Login CSP', type='inf')
                masterkey: str = self.tmp_session.prompt()
                if self.data_mgmt.check_master_key(masterkey):
                    del masterkey
                    return True
                attempts -= 1
                self.vs.print(
                    f'Incorrect masterkey. Attempts remaining: {attempts}',
                    type='err',
                    end='\n'
                )
            except KeyboardInterrupt: continue
            except EOFError: self._exit_csp()
        self.vs.print(f'It has exceeded attempts', type='err')
        return False
    
    def detect_mode(
            self,
            args: Namespace
    ) -> Union['PromptCSP', 'InteractiveCSP', 'OneLinerCPS']:
        """
        Detects the mode specified in the arguments and returns an instance
        of the corresponding class.

        Args:
            args (Namespace): The arguments passed to the method.

        Returns:
            Union[PromptCSP, InteractiveCSP, OneLinerCPS]: An instance of the
            class corresponding to the detected mode.
        """
        match args.mode:
            case 'prompt': return PromptCSP()
            case 'interactive': return InteractiveCSP()
            case _: return OneLinerCPS(args)
    
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
        raw_data = self.data_mgmt.list_data()
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
        field, data_to_find = args
        raw_data = self.data_mgmt.list_data(field, data_to_find)
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
        site: str = None
        username: str = None
        password: str = None
        if len(args) == 3:
            site, username, password = args
        elif len(args) == 2:
            username, password = args
        else:
            password = args
        if self.data_mgmt.new_entry(password, site, username):
            self.vs.print(
                f'Data inserted correcly', 
                type='inf'
            )

    def _delete(self, args: str) -> None:
        """
        Delete data from the database based on the provided id. If the provided
        id not exists end the method, printing a error message.

        Args:
            args (List[str]): Content the id of the data to be deleted.

        Return:
            None: print a message if exec was success or not.
        """
        id: str = args[0]
        if not self._check_exists_id(id):
            return None
        if self.data_mgmt.delete_data(id):
            self.vs.print(
                'Data Deleted Correctly',
                type='inf'
            )

    def _update(self, args: List[str]) -> None:
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
        field: str = args[0]
        data_upd: str = args[1]
        id: int = args[2]
        if not self._check_exists_id(id):
            return None
        if self.data_mgmt.update_data(field, data_upd, id):
            self.vs.print(
                'Data Updated Correctly',
                type='inf'
            )

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
        self.vs.print(f'{reforce_pass} -> copied to clipboard', type='proc')
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
            f'The id: {id} does not exist, and therefore cannot be remove',
            type='err'
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
        self.vs.print('Exiting..', type='err')
        exit(0)

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

    def _proc_instruction(self, instruction: str) -> Tuple[str, List[str]]:
        command, *args = instruction.strip().split(' ')
        args = list(filter(lambda arg: arg != '', args))
        return (command, args)

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
    
class InteractiveCSP(StartCSP):
    def __init__(self) -> None:
        super().__init__()
    
    def start_mode(self):
        pass

class OneLinerCPS(StartCSP):
    def __init__(self, args: Namespace) -> None:
        super().__init__()
        self.args = args
    
    def start_mode(self):
        pass