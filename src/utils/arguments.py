# str library
from typing import Union
from argparse import ArgumentParser, Namespace, _SubParsersAction

# own libraries
from modules.Visuals import Visuals
from modules.Prompt import StartPrompt
from modules.Interactive import Interactive

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
    # add supparsers to operation mode
    mode_subparser: _SubParsersAction = parser.add_subparsers(
        dest='mode', 
        required='False',
        help='Starts the selected operational mode'
    )

    # prompt subparser
    prompt_parser = mode_subparser.add_parser(
        'prompt',
        help='Activate prompt mode for password management',
    )
    prompt_parser.set_defaults(prompt=False)

    # interactive subparser
    interactive_parse = mode_subparser.add_parser(
        'interactive',
        help='Activate interactive mode for password management'
    )
    interactive_parse.set_defaults(interactive=False)

    # general args
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
    args = parser.parse_args()
    return args

# DEPRECATED
def check_and_set_args(args: Namespace) -> str:
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
    vs: Visuals = Visuals()
    password: str = ''
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