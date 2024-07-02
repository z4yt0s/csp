# std libraries
from typing import Dict, List

# thrid party libraries
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.completion import NestedCompleter

# own libraries
from modules.Visuals import Visuals

# PRINTER FUNTIONS
def welcome_msg() -> None:
    """
    Display the welcome message and requirements for the CSP application.
    """
    vs: Visuals = Visuals()
    welcome: str = 'The first time cps is run, a master key must be created'
    func_masterkey0: str = 'The master key will be used to encrypt passwords'
    func_masterkey1: str = 'and as an authentication method'
    title_req: str = 'The master key must have the following requirements'
    req: List[str]= [
        'Minimum length of eight characters',
        'At least one upper and one lower case letter',
        'Contain at least one number',
        'At least one special character',
    ]
    vs.print(welcome, type='inf')
    vs.print(f'{func_masterkey0} {func_masterkey1}', type='inf', end='\n')
    vs.print(title_req, type='war')
    vs.print(req, type='list')