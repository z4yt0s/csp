# std libraries
from typing import Dict, List

# thrid party libraries
from prompt_toolkit.keys import Keys
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.completion import NestedCompleter

# own libraries
from modules.Visuals import Visuals

# KEYBINDING FUNCTIONS
def set_tmp_kb() -> KeyBindings:
    """
    Set temporary keybindings for handling control+c and control+l events.

    Returns:
        KeyBindings: The configured keybindings.
    """
    tmp_kb: KeyBindings = KeyBindings()
    # ctrl + c
    @tmp_kb.add(Keys.ControlC)
    def stop_current_exec(event):
        raise KeyboardInterrupt
    # ctrl + l
    @tmp_kb.add(Keys.ControlL)
    def stop_current_exec(event):
        raise KeyboardInterrupt
    # ctrl + d
    @tmp_kb.add(Keys.ControlD)
    def stop_execution(event):
        raise KeyboardInterrupt('ControlD')
    return tmp_kb

def set_csp_kb() -> KeyBindings:
    """
    Set keybindings specific to the CSP application for control+c and control+d events.

    Returns:
        KeyBindings: The configured keybindings.
    """
    csp_kb: KeyBindings = KeyBindings()
    # ctrl + c
    @csp_kb.add(Keys.ControlC)
    def stop_current_exec(event):
        event.app.current_buffer.delete_before_cursor(1000000)
        event.app.current_buffer.insert_text('^C')
        event.app.current_buffer.validate_and_handle()
    # ctrl + d
    @csp_kb.add(Keys.ControlD)
    def exit_csp(event):
        event.app.current_buffer.delete_before_cursor(1000000)
        event.app.current_buffer.insert_text('exit')
        event.app.current_buffer.validate_and_handle()
    return csp_kb

# COMPLETER FUNCTIONS
def set_completer() -> NestedCompleter:
    """
    Set the completer for CSP application commands.

    Returns:
        NestedCompleter: The configured completer.
    """
    CSP_COMPLETER: Dict[str, Dict[str, None]] = {
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
        'upd': {
            'site': None,
            'username': None,
            'password': None,
        },
        'changemasterkey': None,
        'reforcepass': None,
        'exit': None,
        'help': {
            'list': None,
            'add': None,
            'del': None,
            'upd': None,
            'help': None,
        }
    }
    return NestedCompleter.from_nested_dict(CSP_COMPLETER)

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