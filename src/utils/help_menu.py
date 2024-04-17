# str libraries
from typing import Iterable, Optional, Union, Dict, List

# thrid-party libraries
from rich.text import Text
from rich.style import StyleType
from rich.console import JustifyMethod, Group
from rich.panel import Panel

# f
from modules.Visuals import Visuals

MAIN_HELP: Dict[str, Union[Dict[str, str], List]] = {
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
LIST_HELP: Dict[str, Union[Dict[str, str], str]] = {
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
ADD_HELP: Dict[str, Union[Dict[str, str], List[str]]] = {
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
UPD_HELP: Dict[str, Union[Dict[str, str], str]] = {
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
        'Update the password for a specific entry:': ' CSP> update password 3X4mpl3 3'
    }
}
DEL_HELP: Dict[str, Union[Dict[str, str], str]] = {
    'description': [
        'The delete command allows you to remove data from the',
        'password database based on the provided id.'
    ],
    'usage': ['del {id} | {id1} {id2} ...'],
    'arguments': {
        'id': 'The identifier of the data to be deleted'
    },
    'examples': {
        'Delete an entry with a specific id:': ' CSP> delete 7\n',
        'Delete multiple entries with specific ids:': ' CSP> delete 4 5 9'
    }
}
CRFTP_HELP: Dict[str, Union[Dict[str, str], str]] = {
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
CHMK_HELP: Dict[str, Union[Dict[str, str], str]] = {
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

def create_general_menus(
    DICT_TEXT:  Dict[str, Union[Dict[str, str], List[str]]],
    main:       bool = False
) -> Panel:
    vs: Visuals = Visuals()
    if main:
        # add format to text
        inf_text: Text = list_to_text(
            DICT_TEXT['inf'],
            style='yellow',
            justify='full'
        )
        commands_text: Text = dict_to_text(
            DICT_TEXT['commands'],
            style=['green', 'orange', 'i_purple']
        )
        shortcuts_text: Text = dict_to_text(
            DICT_TEXT['shortcuts'],
            style=['pink', 'orange', 'i_blue']
        )
        # add individual panels
        inf_panel = vs.create_panel(
            inf_text,
            title='info',
            title_align='r',
            border_style=vs.COLORS['i_dark_yellow']
        )
        commands_panel = vs.create_panel(
            commands_text,
            title='commands',
            title_align='r',
            border_style= vs.COLORS['i_dark_green']
        )
        shortcuts_panel = vs.create_panel(
            shortcuts_text,
            title='shorcuts',
            title_align='r',
            border_style=vs.COLORS['i_dark_pink']
        )
        # create panel group
        panel_group = vs.create_panel(renderable=[
            inf_panel,
            commands_panel,
            shortcuts_panel
        ])
        # create final panel
        return vs.create_panel(
            panel_group,
            title='help menu',
            border_style=vs.COLORS['i_grey'],
            padding=(0, 0),
            width=70
        )
    
    description_text: Text = list_to_text(
        DICT_TEXT['description'],
        style='yellow',
        justify='full'
    )
    usage_text: Text = list_to_text(
        DICT_TEXT['usage'],
        style='i_orange'
    )
    arguments_text: Text = dict_to_text(
        DICT_TEXT['arguments'],
        ['green', 'orange', 'i_purple']
    )
    examples_text: Text = dict_to_text(
        DICT_TEXT['examples'],
        style=['pink', 'grey', 'i_blue'],
        separator='\n'
    )

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
    arguments_panel: Panel = vs.create_panel(
        arguments_text,
        title='options',
        title_align='r',
        border_style=vs.COLORS['i_dark_green']
    )
    examples_panel: Panel = vs.create_panel(
        examples_text,
        title='examples',
        title_align='r',
        border_style=vs.COLORS['i_dark_pink']
    )
    panel_group: Group = vs.create_panel(renderable=[
        description_panel,
        usage_panel,
        arguments_panel,
        examples_panel
    ])
    return vs.create_panel(
        panel_group,
        title='list',
        border_style=vs.COLORS['i_grey'],
        padding=(0, 0),
        width=70
    )