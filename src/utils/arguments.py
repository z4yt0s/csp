# str library
from typing import Union
from argparse import ArgumentParser, Namespace, _SubParsersAction

# own libraries
from modules.Visuals import Visuals

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
    parser: ArgumentParser = ArgumentParser(add_help=False)
    # add supparsers to operation mode
    mode_subparser: _SubParsersAction = parser.add_subparsers(
        dest='mode', 
        required='False',
    )

    # prompt subparser
    prompt_parser: _SubParsersAction = mode_subparser.add_parser(
        'prompt',
        add_help=False
    )
    prompt_parser.set_defaults(prompt=False)

    oneliner_parser: _SubParsersAction = mode_subparser.add_parser(
        'oneliner',
        add_help=False
        #allow_abbrev=''
    )
    oneliner_parser.set_defaults(oneliner=False)

    # general args
    oneliner_parser.add_argument(
        '-h', '--help',
        action='store_true',
        default=False
    )
    oneliner_parser.add_argument(
        '-cm', '--change-masterkey',
        action='store_true',
        default=False,
    )
    oneliner_parser.add_argument(
        '-cr', '--craft-password',
        action='store',
        nargs='+',
        type=str,
        metavar='',
        default=None,
    )
    oneliner_parser.add_argument(
        '-x', '--execute',
        action='store',
        type=str,
        metavar='',
        default=None,
    )
    oneliner_parser.add_argument(
        '-a', '--add',
        action='store',
        nargs='+',
        type=str,
        metavar='',
        default=None,
    )
    oneliner_parser.add_argument(
        '-u', '--update',
        action='store',
        nargs='+',
        type=str,
        metavar='',
        default=None,
    )
    oneliner_parser.add_argument(
        '-d', '--delete',
        action='store',
        nargs='+',
        type=str,
        metavar='',
        default=None,
    )
    oneliner_parser.add_argument(
        '-l', '--list',
        action='store',
        nargs='+',
        type=str,
        metavar='',
        default=None,
    )
    args = parser.parse_args()
    return args
