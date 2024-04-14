from typing import Iterable, Optional, Union, Dict, List

from rich.text import Text
from rich.style import StyleType
from rich.console import JustifyMethod

MAIN_HELP: Dict[str, Union[Dict[str, str], List]] = {
    'shortcuts': {
        'Control + L': 'clear the screen',
        'Control + C': 'stop the current procces',
        'Control + D': 'exits the tool',
    },
    'commands': {
        'list': 'list all or specific data',
        'add': 'add a new entry',
        'upd': 'modifies field\'s value in a record',
        'del': 'deletes values from the record',
        'crftp': 'crafts a password based on a phrase',
        'chmk': 'change the masterkey',
        'exit': 'exits the tool [Control + D]',
        'help': 'print the help menu'
    },
    'inf': [
        'If you\'d like more information about available commands,',
        'including examples and options, simply enter the command',
        '\'help [command name]\' to view more details.'
    ]
}

def dict_to_text(
    data:       Dict[str, str],
    style:      Iterable,
    separator:  str='->'
) -> Text:
    text: Text = Text()
    text_styled: List[Text] = []
    counter: int = 0
    length: int = len(data) - 1
    for key, description in data.items():
        line = Text()
        line.append_text(Text(f'{key}\t', style=style[0]))
        line.append_text(Text(f'{separator} ', style=style[1]))
        if counter == length:
            line.append_text(Text(f'{description}', style=style[2]))
            text_styled.append(line)
            break
        line.append_text(Text(f'{description}\n', style=style[2]))
        text_styled.append(line)
        counter += 1

    text = Text()
    for style in text_styled:
        text.append_text(style)
    return text

def list_to_text(
    data:       List[str],
    style:      StyleType,
    justify:    Optional[JustifyMethod] = None,
) -> Text:
    return Text(' '.join(line for line in data), style=style, justify=justify)