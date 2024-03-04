# author: z4yt0s
# date: 02.29.2024
# github: https://github.com/z4yt0s/csp

from typing import NoReturn
from argparse import Namespace
from signal import signal, SIGINT
from sys import exit

from modules.CreateSecurePassword import CreateSecurePasswords
from modules.Visuals import Visuals
from utils.arguments import start_args, check_and_set_args

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