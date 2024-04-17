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
LIST_HELP: Dict[str, Union[Dict[str, str], str]] = {
    'description': [
        'The list command allows you to display data from the password',
        'database. You can either list the entire database or perform'
        'a specific query to find particular data.'
    ],
    'options': [
        'To list the entire database:',
        '\tCSP> list',
        'To perform a specific query:',
        '\t[field]: The field you want to search',
        '\t[data]: The specific data you want to find',
        '\tCSP> list [field] [data]'
    ],
    'usage': ['list [\{field, data\}]'],
    'examples': [
        'List the entire database:'
        '\tCSP> list',
        'Find passwords for a specific id, user, site or password'
        '\tCPS> list id 8',
        '\tCPS> list site github',
        '\tCPS> list username zaytos',
        '\tCPS> list password P4$$w0rd',
    ]
}
ADD_HELP: Dict[str, Union[Dict[str, str], List[str]]] = {
    'description': [
        'The add command allows you to create a new entry',
        'in the password database.'
    ],
    'arguments': {
        'site': 'The name of service associated with the password',
        'username': 'The account name associated with the password',
        'password': 'The password for the website or service'
    },
    'usage': ['add [\{site\}, \{username\}] {password}'],
    'examples': [
        'Add a new entry with site, username, and password:'
        '\tCSP> add github keanu wakeupneo'
        'Add a new entry with username and password only:',
        '\tCSP> add r4ker iloveyou.exe',
        'Add a new entry with only a password:',
        '\tCSP> add idkthepasswordtoset'
    ]
}
UPD_HELP: Dict[str, Union[Dict[str, str], str]] = {
    'description': [
        'The update command allows you to modify data in the password'
        'database based on the provided field, new data, and id.'
    ],
    'arguments': {
        'field': 'The field to update',
        'new_data': 'The new data to replace the existing data',
        'id': 'The identifier of the data to be updated'
    },
    'usage': ['update \{field\} \{new_data\} \{id\}'],
    'examples': [
        'Update the password for a specific entry:'
        '\tCSP> update password new_password 123'
    ]
}
DEL_HELP: Dict[str, Union[Dict[str, str], str]] = {
    'description': [
        'The delete command allows you to remove data from the',
        'password database based on the provided id.'
    ],
    'arguments': {
        'id': 'The identifier of the data to be deleted'
    },
    'usage': ['del \{id\} | \{id1\} \{id2\} ...'],
    'examples': [
        'Delete an entry with a specific id:',
        '\tCSP> delete 7',
        'Delete multiple entries with specific ids:',
        '\tCSP> delete 4 5 9'
    ]
}
CRFTP_HELP: Dict[str, Union[Dict[str, str], str]] = {
    'description': [
        'The crftp (CraftPassword) command converts a phrase into a stronger',
        'password by generating a password using CSP algorithm.'
    ],
    'arguments': {
        'phrase': 'The phrase to be converted into a password',
        'separator': 'Use to identifying words in the phrase (Def: space)'
    },
    'usage': ['crftp \{phrase\} [separator]'],
    'examples': [
        'Reinforce a password with default separator:',
        '\tCSP> crftp i like python and rust',
        'Reinforce a password with custom separator:',
        '\tCPS> reforcepass i_dont_like_java _'
    ]
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