# author: z4yt0s
# date: 02.29.2024
# github: https://github.com/z4yt0s/csp

from typing import ClassVar, List

from rich.console import Console
from rich.align import Align
from rich.table import Table
from rich.text import Text
from rich.theme import Theme

class Visuals:
    """
    Visuals: Handles setting, preparing and rendering all visual elements of the
    tool (tables, alignments, colours, banners, etc).
    
    Attributes:
        CONSOLE_THEME (ClassVar[Theme]): Set the default theme for the console.
    """
    CONSOLE_THEME: ClassVar[Theme] = Theme({
        'green': 'bold green4',
        'blue': 'bold dodger_blue3',
        'purple': 'bold purple4',
        'yellow': 'bold gold3'
    })
    def __init__(self) -> None:
        """
        Initialize the instance of Visuals class.

        Attributes:
            console (Console): Instance of rich.Console for handling console output.
        """
        self.console: Console = Console(
            color_system='256', 
            tab_size=4,
            theme=Visuals.CONSOLE_THEME
        )
    
    def banner(self) -> None:
        """
        Display the banner of the tool
        """
        text_name: Text = Text()
        text_logo: Text = Text()
        text_footern: Text = Text()

        name: List[str] = [
            '                               \n'
            '  /$$$$$$$  /$$$$$$$  /$$$$$$  \n',
            ' /$$_____/ /$$_____/ /$$__  $$ \n',
            '| $$      |  $$$$$$ | $$  \\ $$\n',
            '| $$       \\____  $$| $$  | $$\n',
            '|  $$$$$$$ /$$$$$$$/| $$$$$$$/ \n',
            ' \\_______/|_______/ | $$____/ \n',
            '                    | $$       \n',
            '                    | $$       \n',
            '                    |__/       \n'
        ]
        logo: List[str] = [
            '                  \n'
            '    .-""-.        \n',
            '   / .--. \\      \n',
            '  | |    | |      \n',
            '  | |.-""-.|      \n',
            ' ///`.::::.`\\    \n',
            '||| ::/  \\:: ;   \n',
            '||| ::\\__/:: ;   \n',
            ' \\\\\\ \'::::\' /\n',
            '  `=\'--..-\'`    \n'
        ]
        footern: List[str] = [
            '===============================================\n',
            '  Create Secure Password - created by: z4yt0s\n'
        ]

        for line in name:
            text_name.append(f'{line}', style='bold green4')
        for line in logo:
            text_logo.append(f'{line}', style='bold dodger_blue3')
        for line in footern:
            text_footern.append(f'{line}', style='bold purple4')
        
        table_banner: Table = Table.grid(padding=2)
        table_banner.add_column(no_wrap=2)
        table_banner.add_row(
            Align(text_name, vertical='middle'),
            Align(text_logo, vertical='middle'),
        )
        self.console.print(table_banner)
        self.console.print(text_footern)