# author: z4yt0s
# date: 02.29.2024
# github: https://github.com/z4yt0s/csp

from typing import NoReturn
from argparse import Namespace
from signal import signal, SIGINT
from sys import exit

from modules.CreateSecurePassword import CreateSecurePasswords
from modules.Visuals import Visuals
from modules.StartModes import StartCSP
from utils.arguments import start_args

def main() -> NoReturn:
    args: Namespace = start_args()
    start_csp: StartCSP = StartCSP()
    
    mode = start_csp.detect_mode(args)
    mode.start_mode()

    #password = check_and_set_args(args, vs)
    #csp: CreateSecurePasswords = CreateSecurePasswords(password, args.separator)
    #force_password = csp.create_strong_pass()
    #vs.console.print(f'[bold green4][+] Final Password: {force_password}[/bold green4]')

if __name__ == '__main__':
    main()