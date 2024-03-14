# author: z4yt0s
# date: 03.08.2024
# github: https://github.com/z4yt0s/csp

# str libraries
from typing import (
    Union,
    ClassVar,
    NoReturn,
    Tuple,
    List,
    Dict,
)
from dataclasses import dataclass

# thrid party library
from prompt_toolkit import prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import NestedCompleter as NestComp
from prompt_toolkit.shortcuts import CompleteStyle
#from prompt_toolkit.styles import Style
from prompt_toolkit.cursor_shapes import CursorShape

# own libraries
from DataManagement import DataManagement
from Visuals import Visuals

# POSIBLE FEATURE
# Implements posible dataclass to storage the info referents to 
# info checkers, master_key exits, cred, etc
#@dataclass(frozen=True)

class StartPrompt:
    """
    StartPrompt: Manages the initialization and execution of the CSP start prompt.

    Attributes:
        credentials (ClassVar[bool]): Indicates whether the user has entered
        valid credentials.
    """
    credentials: ClassVar[bool] = False

    def __init__(self) -> None:
        """
        initialize the instance of class StartPrompt.

        Attributes:
            visuals (Visuals): start the instance of Visual.
            data_management (DataManagement): start the instance of DataManagement.

        Description:
            The StartPrompt class initializes visual elements for console 
            interaction, checks for the existence of a master key, initializes
            data_management the driver of database, verifies user credentials,
            and starts a prompt session for user interaction.
        """
        self.visuals: Visuals = Visuals()

        if not DataManagement.masterkey_exists():
            StartPrompt._set_masterkey()

        self.data_management: DataManagement = DataManagement()
        if not StartPrompt.credentials:
            StartPrompt.credentials = self._check_credential()

        self.start_prompt()
    
    @classmethod
    def _set_masterkey(cls) -> DataManagement:
        """
        @CLASSMETHOD
        Sets the master key in case it does not exits in the database.

        Returns:
            DataManagement: DataManagement instance with the set master key.
        """
        masterkey0: str
        visuals = Visuals()
        while True:
            visuals.console.print(
                '[*] The first time you start CSP, you have to create your master key.',
                style='blue'
            )
            visuals.console.print('[^] Enter The Password:', style='green')
            masterkey0: str = cls._credentials_prompt(' ')
            visuals.console.print('[^] Enter The Password:', style='green')
            masterkey1: str = cls._credentials_prompt('[^] Enter The Password: ')
            if masterkey0 != masterkey1:
                print('[!] Passwords must be the same')
                continue
            break
        data_management = DataManagement(masterkey0)
        return data_management
        
    @classmethod
    def _credentials_prompt(cls, msg: str):
        """
        @CLASSMETHOD
        Prompts the user for credentials in a secure manner.

        Args:
            msg (str): The message to display as the prompt.

        Returns: 
            The entered credentials.
        """
        text: str = prompt(msg, is_password=True, cursor=CursorShape.BEAM) # clip? style?
        return text

    def _check_credential(self) -> bool:
        """
        Checks the validity of the entered master key. With a maximum of three
        typing errors.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        self.visuals.console.print('[*] Loading StartPrompt...', style='blue')
        attempts: int = 3
        while attempts > 0:
            self.visuals.console.print('[^] Enter the MasterKey:', style='green')
            masterkey = StartPrompt._credentials_prompt('')
            if self.data_management.check_master_key(masterkey):
                del masterkey
                return True
            attempts -= 1
            self.visuals.console.print(
                f'[!] Incorrect MasterKey. Attempts remaining: {attempts}\n',
                style='red'
            )
        self.visuals.console.print(f'[!] It has exceeded attempts', style='red')
        return False

    def start_prompt(self) -> NoReturn:
        """
        The start_prompt method sets up the interaction interface for the CSP.
        It checks the validity of the user's credentials and starts a loop in
        which it continuously prompts the user for the CSP command line interface.
        The method uses a PromptSession to create and configure the prompt with 
        the various options. Finally these entered commands are sent to the 
        Commands class to process the instruction.
        
        Atributes:
            commands (Commands): instace of Commands, who manages the operations
            and commands inside the CSP.
            csp_session (PromptSession): instance of PromptSession, who provides
            an interface to interact with the user.

        Return:
            NoReturn: ends the execution of the tool
        """
        if not StartPrompt.credentials: return

        commands: Commands = Commands(self.data_management)
        csp_session: PromptSession = PromptSession(
            completer=NestComp.from_nested_dict(Commands.CSP_COMPLETER),
            complete_style=CompleteStyle.READLINE_LIKE,
            cursor=CursorShape.BEAM,
            mouse_support=True
        )
        while True:
            instruction: str = csp_session.prompt('CSP> ')
            commands.check_command(instruction)
    
    def exit_prompt(self) -> NoReturn:
        """
        Securely kills the connection to the database and exits the tool.

        Return:
            NoReturn: ends the execution of the tool
        """
        self.data_management.save_and_exit(exit=True)
        self.visuals.console.print(f'[*] Saving Data...', style='blue')
        self.visuals.console.print(f'[!] Exiting...', style='red')
        exit(0)
    
class Commands:
    CSP_COMPLETER: ClassVar[Dict[str, Dict[str, None]]] = {
        'list': {
            'id': None,
            'site': None,
            'username': None,
            'password': None,
        },
        'add': {
            'site': None,
            'username': None,
            'password': None,
        },
        'del': None,
        'upd':{
            'site': None,
            'username': None,
            'password': None,
        },
        'exit': None,
        'help': {
            'list': None,
            'add': None,
            'del': None,
            'upd': None,
            'help': None,
        }
    }

    def __init__(self, data_management: DataManagement) -> None:
        self.data_management = data_management
        self.visuals = Visuals()

    def check_command(self, instruction: str):
        command, *args = instruction.split(' ')[:4]
        match command:
            case 'list':
                self.list(args)
            case 'add':
                self.add(args)
            case 'del':
                self.delete(args)
            case 'upd':
                self.update(args)
            case 'help':
                self.help()
            case 'exit':
                self.exit_prompt()
            case None:
                pass
            case _:
                self.visuals.console.print(
                    '[!] Command Not Found: try [CSP> help]', 
                    style='red'
                )
    
    def help(self):
        self.visuals.console.print('------------------', style='blue')
        self.visuals.console.print('- Valid Commands -', style='blue')
        self.visuals.console.print('------------------', style='blue')
        self.visuals.console.print('list     list the login data', style='blue')
        self.visuals.console.print('add      create new entry in database', style='blue')
        self.visuals.console.print('exit     exit from tool', style='blue')
        self.visuals.console.print('help     show help for commands', style='blue')
    
    def list(self, args: List[str]):
        # check the raw_data previus render table (IMPLEMENTS TOMORROW)
        args = args[:2]
        if len(args) == 2:
            field: str; data_to_find: str; raw_data: List[Tuple[Union[str, int]]]
            field, data_to_find = args
            raw_data = self.data_management.list_data(field, data_to_find)
            self.visuals.render_table_db(raw_data)
            return
        raw_data = self.data_management.list_data()
        self.visuals.render_table_db(raw_data)

    def add(self, args: List[str]):
        site: str = None
        username: str = None
        password: str = None
        args = args[:3]
        if len(args) == 3:
            site, username, password = args
        elif len(args) == 2:
            username, password = args
        else:
            password = args
        if self.data_management.new_entry(password, site, username):
            self.visuals.console.print(
                f'[*] Data inserted correcly\n', 
                style='blue'
            )

    def update(self, args: List[Union[str, int]]):
        field: str = args[0]
        data_upd: str = args[1]
        id: int = args[2]

        if self.data_management.update_data(field, data_upd, id):
            self.visuals.console.print(
                '[*] Data Updated Correctly',
                style='blue'
            )

    def delete(self, args: List[str]):
        id: int = args[0]

        if self.data_management.delete_data(id):
            self.visuals.console.print(
                '[*] Data Deleted Correctly',
                style='blue'
            )
    
    def exit_prompt(self):
        self.visuals.console.print(
            '[*] Closing connection to database.',
            style='yellow'
        )
        self.data_management.save_and_exit(True)
        self.visuals.console.print(
            '[!] Exiting...',
            style='red'
        )
        exit(0)
            
prompt = StartPrompt()