# author: z4yt0s
# date: 02.29.2024
# github: https://github.com/z4yt0s/csp

from typing import Union, NoReturn, ClassVar, Dict, List, Tuple
from argparse import ArgumentParser, Namespace
from signal import signal, SIGINT
from sys import exit

from rich.console import Console
from rich.align import Align
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

class Visuals:
    """
    Visuals: Handles setting, preparing and rendering all visual elements of the
    tool (tables, alignments, colours, banners, etc).
    
    Attributes:
        CONSOLE_THEME (ClassVar[Theme]): Set the default theme for the console.
    """
    CONSOLE_THEME: ClassVar[Theme] = Theme({
        'green': 'bold green4',
        'blue': 'bold dodger_blue3',
        'purple': 'bold purple4',
        'yellow': 'bold gold3'
    })
    def __init__(self) -> None:
        """
        Initialize the instance of Visuals class.

        Attributes:
            console (Console): Instance of rich.Console for handling console output.
        """
        self.console: Console = Console(
            color_system='256', 
            tab_size=4,
            theme=Visuals.CONSOLE_THEME
        )
    
    def banner(self) -> None:
        """
        Display the banner of the tool
        """
        text_name: Text = Text()
        text_logo: Text = Text()
        text_footern: Text = Text()

        name: List[str] = [
            '                               \n'
            '  /$$$$$$$  /$$$$$$$  /$$$$$$  \n',
            ' /$$_____/ /$$_____/ /$$__  $$ \n',
            '| $$      |  $$$$$$ | $$  \\ $$\n',
            '| $$       \\____  $$| $$  | $$\n',
            '|  $$$$$$$ /$$$$$$$/| $$$$$$$/ \n',
            ' \\_______/|_______/ | $$____/ \n',
            '                    | $$       \n',
            '                    | $$       \n',
            '                    |__/       \n'
        ]
        logo: List[str] = [
            '                  \n'
            '    .-""-.        \n',
            '   / .--. \\      \n',
            '  | |    | |      \n',
            '  | |.-""-.|      \n',
            ' ///`.::::.`\\    \n',
            '||| ::/  \\:: ;   \n',
            '||| ::\\__/:: ;   \n',
            ' \\\\\\ \'::::\' /\n',
            '  `=\'--..-\'`    \n'
        ]
        footern: List[str] = [
            '===============================================\n',
            '  Create Secure Password - created by: z4yt0s\n'
        ]

        for line in name:
            text_name.append(f'{line}', style='bold green4')
        for line in logo:
            text_logo.append(f'{line}', style='bold dodger_blue3')
        for line in footern:
            text_footern.append(f'{line}', style='bold purple4')
        
        table_banner: Table = Table.grid(padding=2)
        table_banner.add_column(no_wrap=2)
        table_banner.add_row(
            Align(text_name, vertical='middle'),
            Align(text_logo, vertical='middle'),
        )
        self.console.print(table_banner)
        self.console.print(text_footern)

class CreateSecurePasswords:
    """
    CreateSecurePasswords: Handles the creation of strong passwords based on a]
    given phrase pattern.

    Attrubutes:
        DICTIONARY_LETTER (ClassVar[Dict[str, str]]): A dictionary mapping specific
        letters to their corresponding replacements for creating strong passwords.
    """
    DICTIONARY_LETTER: ClassVar[Dict[str, str]] = {
        'a': '4',
        'e': '3',
        'i': '1',
        'o': '0',
        'u': '()',
        's': '$',
    }

    def __init__(self, password: str, separator: str) -> None:
        """
        Initialize the instance of class CreateSecurePassword.

        Args:
            password (str): The password to be strengthened.
            separator (str): The character used as a separator between words.
        
        Attributes:
            chars (Tuple[List[str]]): A tuple contanining list of character obteining
            by splitting the input password using the specified separator
        """
        self.chars: Tuple[List[str]] = [
            [*word] for word in password.split(separator)
        ]

    def create_strong_pass(self) -> str:
        """
        Generate a strong psasword based on the given phrase pattern.

        Returns:
            str: The generated strong password
            
        Description:
            The method iterates throught the characters in each word of the password
            replacing specific letters according to the predifined DICTIONARY_LETTER.
            It also capitalizes the firts letter in each word for additional strength.
        """
        dict_letter = CreateSecurePasswords.DICTIONARY_LETTER
        password: str = ''
        for chars in self.chars:
            caps: bool = False
            for char in chars:
                if char in dict_letter.keys():
                    password += dict_letter.get(char)
                    continue
                if not caps:
                    caps = True
                    password += char.capitalize()
                    continue
                password += char
        return password

def start_args() -> Union[Namespace]:
    """
    Parse command-line arguments and return the parsed arguments.

    Returns:
        Namespace: An object containing parsed command-line arguments.

    Description:
        This function uses argparse to define, parse, and return command-line 
        arguments. It sets up an ArgumentParser with options for specifying the
        separator between words, adding special characters to the password, 
        specifying the password directly, and enabling interactive password
        creation. If the interactive mode is not enabled and no password is 
        provided, the help message is printed, and the program exits.
    """
    parser = ArgumentParser(
        description='Create strong passwords based on a given phrase pattern'
    )
    parser.add_argument(
        '-s', '--separator',
        action='store',
        type=str,
        metavar='',
        default=' ',
        help='Specify the character used as a separator between words [default: space]'
    )
    parser.add_argument(
        '-sc', '--specialchar',
        choices=['begin', 'between', 'end'],
        action='store',
        metavar='',
        help='Adds random special characters to the password'
    )
    parser.add_argument(
        '-p', '--password',
        type=str,
        action='store',
        metavar='',
        help='Specifies the password to be strengthened'
    )
    parser.add_argument(
        '-i', '--interactive',
        action='store_true',
        default=False,
        help='Enable interactive password creation'
    )
    args = parser.parse_args()
    if not args.interactive and args.password is None:
        parser.print_help()
        exit(0)
    return args

def check_and_set_args(args: Namespace, vs: Visuals) -> str:
    """
    Validate and set command-line arguments related to password creation.

    Args:
        args (Namespace): Parsed command-line arguments.
        vs (Visuals): An instance of the Visuals class for console output.

    Returns:
        str: The password to be used for creating a strong password.

    Description:
        This function checks and sets command-line arguments related to password
        creation. If a password is provided directly, it is returned. If interactive
        mode is enabled, the user is prompted to input the separator and the password.
        The function then verifies if the entered password is correct. If not, the 
        interactive mode is enabled, and the process repeats.
    """
    password: str
    if args.password is not None:
        password = args.password
    while True:
        if args.interactive:
            vs.console.print(
                f'[*] Specifies the character separating the words: ',
                style='blue',
                end=''
            )
            args.separator = input()
            vs.console.print(
                f'[*] Introduce the password: ',
                style='blue',
                end=''
            )
            password = input()
        vs.console.print(
            f'[?] The password |{password}| its correct [Y/n]: ',
            style='yellow',
            end=''
        )
        if input().lower() == 'n': 
            args.interactive = True
            continue
        break
    return password

def ctrl_c(sig, frame, vs: Visuals=Visuals()) -> NoReturn:
    """
    Handle Ctrl + C interruption.
    Args:
        sig: The signal number.
        frame: The current stack frame
        vs (Visuals): Instance of Visuals for pretty output
    Return: 
        NoReturn (exit)
    """
    vs.console.print(f'\n[!] Exiting. . .', style='bold red3')
    exit(0)

def main() -> NoReturn:
    signal(SIGINT, ctrl_c)

    vs: Visuals = Visuals()
    vs.banner()

    args: Namespace = start_args()
    password = check_and_set_args(args, vs)

    csp: CreateSecurePasswords = CreateSecurePasswords(password, args.separator)
    force_password = csp.create_strong_pass()

    vs.console.print(f'[bold green4][+] Final Password: {force_password}[/bold green4]')

if __name__ == '__main__':
    main()