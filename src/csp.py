# author: z4yt0s
# github: https://github.com/z4yt0s/csp

from typing import NoReturn
from argparse import Namespace

from modules.StartCSP import StartCSP, vs
from utils.arguments import start_args
from utils.visuals_setup import NAME, LOGO, FOOTERN

def main() -> NoReturn:
    vs.banner(NAME, LOGO, FOOTERN)
    args: Namespace = start_args()
    start_csp: StartCSP = StartCSP()
    
    mode = start_csp.detect_mode(args)
    mode.start_mode()

if __name__ == '__main__':
    main()