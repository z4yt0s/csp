# str libraries
from typing import Iterable, Optional, Union, Dict, List, Any, Tuple

# thrid-party libraries
from rich.text import Text
from rich.style import StyleType
from rich.console import JustifyMethod, Group
from rich.panel import Panel

# f
from modules.Visuals import Visuals

# Prompt Mode
MAIN_HELP: Dict[str, Union[Dict[str, str], List[str], str]] = {
    'title': 'help',
    'inf': [
        'If you\'d like more information about available commands,',
        'including examples and options, simply enter the command',
        '\'help [command name]\' to view more details.'
    ],
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
    'shortcuts': {
        'Control + L': 'clear the screen',
        'Control + C': 'stop the current procces',
        'Control + D': 'exits the tool',
    }

}
LIST_HELP: Dict[str, Union[Dict[str, str], List[str], str]] = {
    'title': 'list',
    'description': [
        'The list command allows you to display data from the password',
        'database. You can either list the entire database or perform'
        'a specific query to find particular data.'
    ],
    'usage': ['list [{field, data}]'],
    'arguments': {
        'field': 'The field you want to search',
        'data': 'The specific data you want to find',
    },
    'examples': {
        'List the entire database:': ' CSP> list\n',
        'Find passwords for a specific id': ' CPS> list id 8\n',
        'Find passwords for a specific site': ' CPS> list site github\n',
        'Find passwords for a specific username': ' CPS> list username zaytos\n',
        'Find passwords fro a specific password': ' CPS> list password P4$$w0rd',
    }
}
ADD_HELP: Dict[str, Union[Dict[str, str], List[str], str]] = {
    'title': 'add',
    'description': [
        'The add command allows you to create a new entry',
        'in the password database.'
    ],
    'usage': ['add [{site}, {username}] {password}'],
    'arguments': {
        'site\t': 'The name of service associated with account',
        'username': 'The account name associated with account',
        'password': 'The password for the website or service'
    },
    'examples': {
        'New entry with site, username, and password:': ' CSP> add github keanu wakeupneo\n',
        'New entry with username and password only:': ' CSP> add r4ker iloveyou.exe\n',
        'New entry with only a password:': ' CSP> add idkthepasswordtoset'
    }
}
UPD_HELP: Dict[str, Union[Dict[str, str], List[str], str]] = {
    'title': 'upd',
    'description': [
        'The update command allows you to modify data in the password'
        'database based on the provided field, new data, and id.'
    ],
    'usage': ['update {field} {new_data} {id}'],
    'arguments': {
        'field\t': 'The field to update',
        'new_data': 'The new data to replace the existing data',
        'id\t': 'The identifier of the data to be updated'
    },
    'examples': {
        'Update the password for a specific entry:': ' CSP> upd password 3X4mpl3 3'
    }
}
DEL_HELP: Dict[str, Union[Dict[str, str], List[str], str]] = {
    'title': 'del',
    'description': [
        'The delete command allows you to remove data from the',
        'password database based on the provided id.'
    ],
    'usage': ['del {id} | {id1} {id2} ... | {id1}..{id5}'],
    'arguments': {
        'id': 'The identifier of the data to be deleted'
    },
    'examples': {
        'Delete an entry with a specific id:': ' CSP> del 7\n',
        'Delete multiple entries with specific ids:': ' CSP> del 4 5 9\n',
        'Delete a range of entries': 'CSP> del 10..15'
    }
}
CRFTP_HELP: Dict[str, Union[Dict[str, str], List[str], str]] = {
    'title': 'crftp',
    'description': [
        'The crftp (CraftPassword) command converts a phrase into a stronger',
        'password by generating a password using CSP algorithm.'
    ],
    'usage': ['crftp {phrase} [separator]'],
    'arguments': {
        'phrase': 'The phrase to be converted into a password',
        'separator': 'Use to identifying words (Def: space)'
    },
    'examples': {
        'CraftPassword with default separator:': ' CSP> crftp i like python and rust\n',
        'CraftPassword with custom separator:': ' CPS> crftp i_dont_like_java _'
    }
}
CHMK_HELP: Dict[str, Union[Dict[str, str], List[str], str]] = {
    'title': 'chmk',
    'description': [
        'The chmk (ChangeMasterkey) command allows you to update your master',
        'key securely. First, you authenticate using your current master key.',
        'Then, you enter your new master key. The command decrypts your',
        'existing passwords using the old master key and encrypts them again',
        'using the new one. This ensures that all your passwords are protected',
        'with the updated master key.'
    ],
    'usage': ['chmk'],
}

# Oneliner Mode
MAIN_HELP_ONELINER: Dict[str, Union[Dict[str, str], List[str]]] = {
    'description': [
        'CSP (Create Secure Password) is a command line tool for secure and',
        'private password management. It stores, retrieves, updates and deletes',
        'passwords in an encrypted database. It also generates strong',
        'passwords to improve the security of your online accounts.'
    ],
    'usage': ['csp.py {prompt oneliner} [-h]'],
    'pos_args': {
        'prompt': 'Interactive mode for password management.',
        'oneliner': 'One-liner mode for quick password operations.'
    }
}

ARGS_HELP_ONELINER: Dict[str, Union[Dict[str, str], List[str], str]] = {
    'usage': ['csp.py oneliner [-cm, -h], [-cr, -x, -a, -u, -d, -l, -sc]'],
    'options': {
        '-cp, --craft-password': 'converts a phrase into a stronger password',
        '-x, --execute\t': 'execute a command of prompt mode',
        '-h, --help\t\t': 'show this help message and exit'
    },
    'crud_options': {
        '-l, --list\t': 'list the fields in database',
        '-a, --add\t': 'adds a new record in database',
        '-d, --delete': 'remove the data in the database',
        '-u, --update': 'update the data in the database'
    },
    'conf_options': {
        '-cm, --change-masterkey': 'change the CSP masterkey',
        '-cl, --change-location': 'modify the path of database file'
    }
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
    return Text(''.join(line for line in data), style=style, justify=justify)

def change_keys(
    DICT_TEXT:  Dict[str, Union[Dict[str, str], List[str]]],
    keys:       Tuple[str],
    style:      Tuple[Union[str, List[str]]]
) -> str:
    try:
        DICT_TEXT[keys[0]]
        return [keys[0], style[0]]
    except KeyError:
        DICT_TEXT[keys[1]]
        return [keys[1], style[1]]

def detect_list_dict(
    DICT_TEXT,
    style,
    justify     = None,
    separator   = '->'
) -> Text:
    match type(DICT_TEXT).__name__:
        case 'list':
            return list_to_text(DICT_TEXT, style=style, justify=justify)
        case 'dict':
            return dict_to_text(DICT_TEXT, style=style, separator=separator)
        case _:
            print('Dato no soportado')

def create_general_menus(
    DICT_TEXT:  Dict[str, Union[Dict[str, str], List[str]]],
    width:      int = 70,
    main:       bool = False,
    oneliner:   bool = False,
) -> Panel:
    vs: Visuals = Visuals()
    if main:
        # add format to text
        key: List[str, Union[str, List[str]]] = change_keys(
            DICT_TEXT,
            keys=('inf', 'description'),
            style=('yellow', 'yellow')
        )
        inf_or_desc_text: Text = detect_list_dict(
            DICT_TEXT[key[0]],
            style=key[1],
            justify='full'
        )

        key: Dict[str, str] = change_keys(
            DICT_TEXT,
            keys=('commands', 'usage'),
            style=(['green', 'orange', 'i_purple'], 'orange')
        )
        commands_or_usage_text: Text = detect_list_dict(
            DICT_TEXT[key[0]],
            style=key[1]
        )

        key: str = change_keys(
            DICT_TEXT,
            keys=('shortcuts', 'pos_args'),
            style=(['pink', 'orange', 'i_blue'], ['green', 'orange', 'i_purple'])
        )
        shortcuts_or_pos_args_text: Text = detect_list_dict(
            DICT_TEXT[key[0]],
            style=key[1]
        )
        
        # add individual panels
        inf_panel = vs.create_panel(
            inf_or_desc_text,
            title='info',
            title_align='r',
            border_style=vs.COLORS['i_dark_yellow']
        )
        commands_or_usage_panel = vs.create_panel(
            commands_or_usage_text,
            title='shorcuts' if not oneliner else 'usage',
            title_align='r',
            border_style=vs.COLORS['i_dark_green']
        )
        shortcuts_or_pos_args_panel = vs.create_panel(
            shortcuts_or_pos_args_text,
            title='shorcuts' if not oneliner else 'positional arguments',
            title_align='r',
            border_style=vs.COLORS['i_dark_pink']
        )
        # create panel group
        panel_group = vs.create_panel(renderable=[
            inf_panel,
            commands_or_usage_panel,
            shortcuts_or_pos_args_panel 
        ])
        # create final panel
        return vs.create_panel(
            panel_group,
            title='help menu' if not oneliner else 'oneliner help',
            border_style=vs.COLORS['i_grey'],
            padding=(0, 0),
            width=width
        )
    if not oneliner:
        description_text: Text = detect_list_dict(
            DICT_TEXT['description'],
            style='yellow',
            justify='full'
        )

    usage_text: Text = detect_list_dict(
        DICT_TEXT['usage'],
        style='i_orange'
    )
    key: str = change_keys(
        DICT_TEXT,
        ('arguments', 'options'),
        style=(['green', 'orange', 'i_purple'], ['green', 'orange', 'i_purple'])
    )
    arguments_or_options_text: Text = detect_list_dict(
        DICT_TEXT[key[0]],
        style=key[1]
    )

    key: str = change_keys(
        DICT_TEXT,
        ('examples', 'crud_options'),
        style=(['pink', 'grey', 'i_blue'], ['pink', 'orange', 'i_blue'])
    )
    examples_or_crud_options_text: Text = detect_list_dict(
        DICT_TEXT[key[0]],
        style=key[1],
        separator='\n' if not oneliner else '->'
    )
    if oneliner:
        conf_options_text: Text = detect_list_dict(
            DICT_TEXT['conf_options'],
            style=['blue', 'orange', 'i_red'],
            separator='\n' if not oneliner else '->'
        )
        conf_options_panel: Panel = vs.create_panel(
            conf_options_text,
            title='conf options',
            title_align='r',
            border_style=vs.COLORS['dark_red']
        )
        
    if not oneliner:
        description_panel: Panel = vs.create_panel(
            description_text,
            title='description',
            title_align='r',
            border_style=vs.COLORS['i_dark_yellow']
        )

    usage_panel: Panel = vs.create_panel(
        usage_text,
        title='usage',
        title_align='r',
        border_style=vs.COLORS['i_dark_orange'],
        padding=(0, 2)
    )
    arguments_or_options_panel: Panel = vs.create_panel(
        arguments_or_options_text,
        title='arguments' if not oneliner else 'options',
        title_align='r',
        border_style=vs.COLORS['i_dark_green']
    )
    examples_or_crud_options_panel: Panel = vs.create_panel(
        examples_or_crud_options_text,
        title='examples' if not oneliner else 'crud options',
        title_align='r',
        border_style=vs.COLORS['i_dark_pink']
    )
    if oneliner:
        panel_group: Group = vs.create_panel(renderable=[
            usage_panel,
            examples_or_crud_options_panel,
            arguments_or_options_panel,
            conf_options_panel
        ])
        return vs.create_panel(
            panel_group,
            title='oneliner options',
            border_style=vs.COLORS['i_grey'],
            padding=(0, 0),
            width=width
        )
    panel_group: Group = vs.create_panel(renderable=[
        description_panel,
        usage_panel,
        arguments_or_options_panel,
        examples_or_crud_options_panel
    ])
    return vs.create_panel(
        panel_group,
        title=DICT_TEXT['title'],
        border_style=vs.COLORS['i_grey'],
        padding=(0, 0),
        width=width
    )