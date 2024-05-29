# str libraries
from typing import (
    ClassVar,
    NoReturn,
    Callable,
    Optional,
    Union,
    Any,
    Tuple,
    List,
    Dict
)
from functools import wraps
from pathlib import Path
from argparse import Namespace
from time import sleep
from signal import signal, SIGINT, SIG_IGN

# third-party libraries
from InquirerPy.prompts.list import ListPrompt
from InquirerPy.utils import get_style
from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.cursor_shapes import CursorShape
from pyperclip import copy

# test
from rich.progress import track
from rich.panel import Panel
from rich.text import Text
from rich.console import Group

# own libraries
from modules.DataManagement import DataManagement
from modules.Visuals import Visuals
from modules.CreateSecurePassword import CreateSecurePasswords # change
from modules.Crypt import PassCrypt
from utils.prompt_config import (
    set_tmp_kb,
    set_csp_kb,
    set_completer,
    welcome_msg
)
from utils.help_menu import (
    dict_to_text,
    list_to_text,
    create_general_menus,
    MAIN_HELP,
    LIST_HELP,
    ADD_HELP,
    UPD_HELP,
    DEL_HELP,
    CRFTP_HELP,
    CHMK_HELP,
    MAIN_HELP_ONELINER,
    ARGS_HELP_ONELINER,
)
from utils.visuals_setup import NAME, LOGO, FOOTERN

vs: Visuals = Visuals()

def create_tmp_session(
    msg:        List[Tuple[str]],
    password:   Optional[bool] = False,
    style:      Optional[Dict[str, str]] = {'msg': Visuals.COLORS['green']}
) -> PromptSession:
    return PromptSession(
        message=msg,
        style=Style.from_dict(style),
        is_password=password,
        key_bindings=set_tmp_kb()
    )

class PathCSP:
    """
    La clase PathCSP se encarga de gestionar y realizar todas las operaciones
    correspondiente a las rutas y ficheros del sistema.
    """
    ROOT_DIR: ClassVar[Path] = Path.home() / '.csp'
    STYLE_OPTIONS: ClassVar[Dict[str, str]] = {
        'questionmark':         f'fg:{Visuals.COLORS["yellow"]}',
        'question':             f'fg:{Visuals.COLORS["yellow"]}',
        'answermark':           f'fg:{Visuals.COLORS["green"]}',
        'answered_question':    f'fg:{Visuals.COLORS["green"]}',
        'answer':               f'fg:{Visuals.COLORS["purple"]} bold',
        'pointer':              f'fg:{Visuals.COLORS["orange"]} bold',
        'fuzzy_border':         f'fg:{Visuals.COLORS["blue"]}',
        'skipped':              f'fg:{Visuals.COLORS["red"]}'
    }

    def __init__(self):
        """
        En primer lugar comprueba si existe la ruta de gestion de ficheros, sino
        la crea, posteriormente detecta si existe ficheros .db, en el caso de que
        no se detecten se generara uno con los parametros indicados por el usuario
        """
        if not PathCSP.ROOT_DIR.exists():
            PathCSP.ROOT_DIR.mkdir()
            
        self.db_files: List[Path] = self._upd_list_files()
        if not self.db_files:
            self.create_db_file()
    
    def _upd_list_files(self) -> List[Path]:
        return sorted(PathCSP.ROOT_DIR.glob('**/*.db'))

    def create_db_file(self) -> None:
        """
        """
        tmp_session: PromptSession = create_tmp_session(
            msg=[('class:msg', '[^] Specify a name the database file: ')],
        )
        # in future add panel for list existing database files

        while True:
            db_name: str = f'{tmp_session.prompt()}.db'
            db_file: Path = PathCSP.ROOT_DIR / db_name
            if db_file in self.db_files:
                vs.print(
                    f'The file {db_file} already exists, choose another name',
                    type='err',
                    end='\n\n'
                ); continue
            db_file.touch()
            DataManagement.create_database(db_file)
            break
        self.db_files = self._upd_list_files()

    def select_databases(self) -> Path:
        if len(self.db_files) == 1:
            return self.db_files[0]
        list_prompt: ListPrompt = ListPrompt(
            message='Select database file:',
            choices=[file.name for file in self.db_files],
            style=get_style(PathCSP.STYLE_OPTIONS),
            qmark='[?]',
            amark='[^]',
            mandatory=False,
            show_cursor=False,
            border=True,
            vi_mode=True,
            keybindings={"skip": [{"key": "c-c"}]}
        )
        path_db: Path = PathCSP.ROOT_DIR / list_prompt.execute()
        print()
        return path_db

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
        self.path_csp: PathCSP = PathCSP()
        self.data_mgmt: Union[None, DataManagement] = None
    
    def need_auth(method: Callable) -> Callable:
        @wraps(method)
        def wrapper(self_cls, *args, **kwargs):
            if not self_cls._authenticated:
                vs.print(
                    'Need authentication in some databases',
                    type='err'
                )
                vs.print(
                    'Try: [CSP> selectdb] for select database',
                    type='war'
                )
                return None
            return method(self_cls, *args, **kwargs)
        return wrapper

    def check_masterkey(self, db_path: Path) -> NoReturn:
        """
        Check if the masterkey exits and realize the user authentication for
        start the tool. In case if all checkers are correct, change the value
        of StartCSP._authenticated to True
        """
        if not self.data_mgmt.masterkey_exists(db_path):
            self.create_and_store_masterkey()
        if not self._check_credentials():
            self._exit_csp()
        StartCSP._authenticated = True
        
    def create_and_store_masterkey(
       self,
       reset: bool = False
    ) -> Union[None, str]:
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
        tmp_session: PromptSession = create_tmp_session(
            msg=StartCSP.AUTH_QUESTION,
            password=True
        )
        while True:
            try:
                masterkey0: str = tmp_session.prompt()
                if masterkey0 != tmp_session.prompt():
                    vs.print(
                        'Password must be the same',
                        type='err',
                        end='\n'
                    )
                    continue
                if not CreateSecurePasswords.is_strong_password(masterkey0):
                    vs.print(
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
        vs.print('Masterkey inserted correctly', type='inf', end='\n')
    
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
        tmp_session: PromptSession = create_tmp_session(
            msg=StartCSP.AUTH_QUESTION,
            password=True
        )
        attempts: int = 3
        while attempts > 0:
            try:
                vs.print('Login CSP', type='inf')
                masterkey: str = tmp_session.prompt()
                if not self.data_mgmt.check_master_key(masterkey):
                    attempts -= 1
                    vs.print(
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
        vs.print(f'It has exceeded attempts', type='err')
        return False
    
    @need_auth
    def _change_masterkey(self) -> None:
        """
        Change the masterkey of the csp database, in this process it checks the
        old masterkey and stores it. Subsequently it gets all the entries from
        database and decrypts them. In this point start the process to set a new
        masterkey. If its create correctly, the old entries decrypted we encrypt
        in base a new masterkey. And show the progress with a bar.
        """
        tmp_session: PromptSession = create_tmp_session(
            msg=StartCSP.AUTH_QUESTION,
            password=True
        )
        signal(SIGINT, SIG_IGN)
        
        # check old masterkey and decrypt all entries of csp database
        vs.print(
            'Executing the masterkey change process..',
            type='inf',
            bad_render=True
        )
        vs.print(
            'Enter the actual masterkey to decryption of existing data.',
            type='inf',
        )
        old_masterkey: str = tmp_session.prompt()
        if not self.data_mgmt.check_master_key(old_masterkey):
            vs.print('The masterkey its invalid', type='err')
            return None
        old_crypt_raw_data = self.data_mgmt.list_data()
        old_raw_data = self._decrypt_listed_data(old_crypt_raw_data)
        
        # create new masterkey and cypher the old_raw_data with new masterkey
        vs.print(
            'Starting the process to create a new masterkey',
            type='inf',
            start='\n'
        )
        new_masterkey = self.create_and_store_masterkey(reset=True)
        StartCSP._passcrypt = PassCrypt(new_masterkey)
        vs.print(
            'Masterkey was created and stored succesfully',
            type='inf'
        )
        vs.print(
            'Beggining the process to encrypt the existing passwords',
            type='inf'
        )
        vs.print(
            f'Numbers of entries detected: {len(old_raw_data)}',
            type='inf',
            bad_render=True
        )
        # render a the progress bar
        for entry in track(old_raw_data, description='[bold blue]Encrypting[/bold blue]'):
            new_data: List[Union[str, int]] = [
                'password',
                entry[3],
                entry[0]
            ]
            self._upd(new_data, skip_msg=True)
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

    @need_auth
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
        vs.render_table_db(raw_data)

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
            vs.print(
                f'The atributes specify are wrong -> {ve}',
                type='err',
                bad_render=True
            )
            vs.print(
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
            vs.print(
                'The requested value was not found in the database',
                type='err'
            )
            return None
        vs.render_table_db(raw_data)

    @need_auth
    def _add(self, args: List[str]) -> None:
        """
        Create a new entry to database, and encrypt password.
        
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

        crypt_raw_pass: Tuple[str] = StartCSP._passcrypt.encrypt(password)
        password = f'{crypt_raw_pass[0]}|{crypt_raw_pass[1]}|{crypt_raw_pass[2]}'
        if self.data_mgmt.new_entry(password, site, username):
            vs.print(
                f'Data inserted correcly', 
                type='inf'
            )

    @need_auth
    def _del(self, args: List[str]) -> None:
        """
        Delete data from the database based on the provided id. If the provided
        id not exists end the method, printing a error message.

        Args:
            args (List[str]): Content the id of the data to be deleted.

        Return:
            None: print a message if exec was success or not.
        """
        def _del_id(id: int) -> bool:
            """
            The function deletes a specific entry of csp database, in base to
            id of the entry. This check if id exists in the record.
            
            Args:
                id (int): the number of id to delete.
                
            Returns:
                bool: False if the id dont exists in record, True if this delete
                successfully.
            """
            if not self._check_exists_id(id): return False
            if self.data_mgmt.delete_data(id):
                vs.print(
                    f'Data Deleted Correctly: id {id}',
                    type='inf',
                    bad_render=True
                )
                return True

        # enumerate, returns an iterable containing (index | value). Each value
        # is checked to see if it contains'..' y filter returns only data matching
        # that condition. Subsequently the function get_range_index is mapped,
        # with the iterable resulting from filter, storing in index_range_mode a
        # list of values of indexes that its syntax follows the range deletion
        # mode. If not detect this mode index_range_mode storaged None value.
        index_range_mode: Union[None, List[int]] = list(map(
            lambda get_range_index: get_range_index[0],
            filter(lambda index_val: '..' in index_val[1], enumerate(args))
        ))

        # normal mode
        for index, id in enumerate(args):
            if index in index_range_mode: continue
            if not _del_id(id): continue

        # range mode
        if index_range_mode is None: return None
        for index in index_range_mode:
            range_ = args[index]
            id_beg, id_end = map(int, range_.split('..'))
            # map() delays execution until needed; but wrapping list around
            # map 'list(map())' forces immediate execution of map object
            list(map(_del_id, range(id_beg, id_end + 1)))

    @need_auth
    def _upd(self, args: List[str], skip_msg: bool = False) -> None:
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
            vs.print(
                f'The atributes specify are wrong -> {ve}',
                type='err',
                bad_render=True
            )
            vs.print(
                'Try: [CSP> help] to see the help menu',
                type='war'
            )
            return None

        if not self._check_exists_id(id): return None
        if field == 'password':
            crypt_data_upd: Tuple[str] = StartCSP._passcrypt.encrypt(data_upd)
            data_upd: str = f'{crypt_data_upd[0]}|{crypt_data_upd[1]}|{crypt_data_upd[2]}'

        if self.data_mgmt.update_data(field, data_upd, id) and not skip_msg:
            vs.print( 'Data Updated Correctly', type='inf')

    def _crftp(self, args: List[str]) -> None:
        """
        Craft-Password a given password by generating a stronger password using
        CreateSecurePasswords class.

        Args:
            args (List[str]): List containing the original password and a
            separator.

        Returns:
            None: This method does not return any value.
        """
        if len(args) > 2:
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
        vs.print('Password reforce succesfull', type='inf')
        if not csp.is_strong_password(reforce_pass):
            msg0: str = 'The generated password does not meet security '
            msg1: str = 'requirements. Use it at your own risk'
            vs.print(f'{msg0}{msg1}', type='war')

        vs.print(
            f'{reforce_pass} -> copied to clipboard',
            type='proc',
            bad_render=True
        )
        copy(reforce_pass)

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

        vs.print(
            f'The id: {id} does not exist, therefore the action cannot be executed',
            type='err',
            bad_render=True
        )
        return False

    def _exit_csp(self, print_msg: bool = True) -> NoReturn:
        """
        Exit the CSP tool. This method prints an exit message, saves an 
        necessary data, and terminates the program

        Return:
            NoReturn: end the program.
        """
        if print_msg:
            vs.print('Save and closing connection to database', type='inf')
        self.data_mgmt.save_and_exit(True)
        if print_msg:
            vs.print('Exiting..', type='err', bad_render=True)
        exit(0)
    
    def _proc_instruction(
        self,
        instruction: Union[str, bool]
    ) -> Union[bool, Tuple[str, List[str]], List[str]]:
        """
        Process the instructions in each mode, this method have three modes:
            Proc True Options:
                If detects bool type return the value of bool instruction.
            PromptCSP:
                In prompt mode we need divide the raw instruction in two parts
                (commands & args), commands is the first part of an instruction,
                and this is esasy to identify, but the args the args have to be
                processed. These are divided by ' ', and the returned in a list
                of words between the spaces.
            OneLinerCSP:
                In oneliner mode, we identify the commands by the use of flags,
                so we are only interested in processing the arguments. In this
                case it is the same method as the previous case. The difference
                is that only the arguments are returned in a list.
        Args:
            instructions (str, bool): instruction to be processed.
        Return:
            bool, True Options
            Tuple(str, List(str)): PromptCSP
            List(str): OnelinerCSP
        """
        if type(instruction).__name__ == 'bool':
            return instruction
        
        son_class: str = type(self).__name__
        if son_class == 'PromptCSP':
            command, *args = instruction.strip().split(' ')
            args: List[str] = list(filter(lambda arg: arg != '', args))
            return (command, args)

        if son_class == 'OneLinerCSP':
            args: List[str] = [
                word for raw_args in instruction
                for word in raw_args.strip().split(' ')
            ]
            args = list(filter(lambda arg: arg != '', args))
            return args

    def _decrypt_listed_data(self, crypt_raw_data: List[Tuple[Any]]) -> List[str]:
        """
        Decrypt the data returned of database in _list or _list_specific method

        Args:
            crypt_raw_data(List(Tuple(Any))): its the data returned of database
            after queried.

        Return:
            List(str): Return a list with all data decrypted and more easier to
            read and iterate
        """
        decrypted_passwords = [
            StartCSP._passcrypt.decrypt(tuple(fields[3].split('|')))
            for fields in crypt_raw_data
        ]
        return [
            list(fields[:3]) + [password]
            for fields, password in zip(crypt_raw_data, decrypted_passwords)
        ]

class PromptCSP(StartCSP):
    """
    The PromptCSP class handles user interaction in the interactive mode of
    the CSP tool. It inherits from the StartCSP class and overrides methods
    to handle user input and execute corresponding actions.
    """
    def __init__(self) -> None:
        """
        Atributes:
            csp_session (PromptSession): PromptSession instance for handling
            user input.
        """
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
        """
        Start the prompt mode of the tool CSP tool.
        """
        while True:
            try:
                instruction: str = self.csp_session.prompt()
                self._check_command(instruction)
            except KeyboardInterrupt:
                self._check_command('^C')

    def _check_command(self, instruction: str) -> None:
        """
        Check and processes the user input.

        Args: 
            instruction (str): User input containing the command and argument.
        """
        command, args = self._proc_instruction(instruction)
        match command:
            case 'list': self._list(args)
            case 'add': self._add(args)
            case 'del': self._del(args)
            case 'upd': self._upd(args)
            case 'crftp': self._crftp(args)
            case 'chmk': self._change_masterkey()
            case 'selectdb':
                db_path: Path = self.path_csp.select_databases()
                self.data_mgmt = DataManagement(db_path)
                self.check_masterkey(db_path)
                self._authenticated = True
            case 'newdb':
                self.path_csp.create_db_file()
            case 'help': self._help(args)
            case 'exit': self._exit_csp()
            case '^C': pass
            case _: vs.print('Command Not Fount: try [CSP> help]', type='err')

    def _help(self, args: List[str]) -> None:
        """
        Displays help information based on specific command.
        
        Args:
            args (List(str)): Command argument for show specific information
            command.
        """
        def _h_chmk():
            """Special panel for command chmk"""
            description_text: Text = list_to_text(
                CHMK_HELP['description'],
                style='yellow',
                justify='full'
            )

            description_panel: Panel = vs.create_panel(
                description_text,
                title='description',
                title_align='r',
                border_style=vs.COLORS['i_dark_yellow']
            )
            panel_group: Group = vs.create_panel(renderable=[
                description_panel
            ])
            return vs.create_panel(
                panel_group,
                title='chmk',
                border_style=vs.COLORS['i_grey'],
                padding=(0, 0),
                width=70
            )

        try: args: str = args[0]
        except IndexError: args: str = 'None'

        match args:
            case 'list': vs.console.print(create_general_menus(LIST_HELP))
            case 'add': vs.console.print(create_general_menus(ADD_HELP))
            case 'upd': vs.console.print(create_general_menus(UPD_HELP))
            case 'del': vs.console.print(create_general_menus(DEL_HELP))
            case 'crftp': vs.console.print(create_general_menus(CRFTP_HELP))
            case 'chmk': vs.console.print(_h_chmk())
            case _: vs.console.print(create_general_menus(MAIN_HELP, main=True))

class OneLinerCSP(StartCSP):
    """
    The OneLinerCSP class handles the one-liner mode of the CSP tool. It
    inherits from the StartCSP class and processes command-line arguments
    to perform actions accordingly.
    """
    def __init__(self, args: Namespace) -> None:
        """
        Args:
            args (Namespace): Namespace containing command-line arguments.
        """
        super().__init__(); print()
        self.args = args
    
    def _help(self, width: int = 85):
        vs.console.print(create_general_menus(
            MAIN_HELP_ONELINER,
            main=True,
            oneliner=True,
            width=width,
        ))
        vs.console.print(create_general_menus(
            ARGS_HELP_ONELINER,
            oneliner=True,
            width=width
        ))
        self._exit_csp(print_msg=False)
    
    def start_mode(self):
        """
        Starts the one-liner mode of the CSP tool and executes actions based on
        the provided command-line arguments.
        """
        for argument, args in self.args.__dict__.items():
            if args is None: continue
            proc_args: Union[List[str], bool] = self._proc_instruction(args)
            match argument:
                case 'help': self._help()

                case 'change_masterkey': 
                    if not proc_args: continue
                    self._change_masterkey()

                case 'craft_password':
                    self._crftp(proc_args)

                case 'execute':
                    tmp_prompt: PromptCSP = PromptCSP()
                    tmp_prompt._check_command(self.args.execute)

                case 'add': self._add(proc_args)
                case 'update': self._upd(proc_args)
                case 'delete': self._del(proc_args)
                case 'list': self._list(proc_args)