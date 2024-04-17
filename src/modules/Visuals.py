# author: z4yt0s
# date: 02.29.2024
# github: https://github.com/z4yt0s/csp
from typing import (
    Literal,
    Optional,
    Iterable,
    Union,
    ClassVar,
    Any,
    Tuple,
    List,
    Dict
)
from time import sleep

from rich.theme import Theme
from rich.console import Console, Group, RenderableType
from rich.text import Text, TextType
from rich.style import Style, StyleType
from rich.table import Table
from rich.align import Align
from rich.live import Live
from rich.panel import Panel
from rich.padding import PaddingDimensions
from rich.box import Box, ROUNDED, DOUBLE_EDGE

class Visuals:
    """
    Visuals: Handles setting, preparing and rendering all visual elements of the
    tool (tables, alignments, colours, banners, etc).
    
    Attributes:
        COLORS (ClassVar[Dict[str, str]])
        CONSOLE_THEME (ClassVar[Theme]): Set the default theme for the console.
    """
    COLORS: ClassVar[Dict[str, str]] = {
        'green':            '#00b44e',
        'blue':             '#0063e2',
        'purple':           '#7f00df',
        'pink':             '#ba1d67',
        'red':              '#bc2920',
        'orange':           '#cd620e',
        'yellow':           '#cac20d',
        'grey':             '#505050',
        'dark_green':       '#227547',
        'dark_blue':        '#2b5893',
        'dark_purple':      '#542d98',
        'dark_pink':        '#792f57',
        'dark_red':         '#712823',
        'dark_orange':      '#8a5429',
        'dark_yellow':      '#858125',
        'b_green':          'bold #00b44e',
        'b_blue':           'bold #0063e2',
        'b_purple':         'bold #8300ff',
        'b_pink':           'bold #ba1d67',
        'b_red':            'bold #bc2920',
        'b_orange':         'bold #cd620e',
        'b_yellow':         'bold #cac20d',
        'b_grey':           'bold #505050',
        'b_dark_green':     'bold #227547',
        'b_dark_blue':      'bold #2b5893',
        'b_dark_purple':    'bold #542d98',
        'b_dark_pink':      'bold #792f57',
        'b_dark_red':       'bold #712823',
        'b_dark_orange':    'bold #8a5429',
        'b_dark_yellow':    'bold #858125',
        'i_green':          'italic #00b44e',
        'i_blue':           'italic #0063e2',
        'i_purple':         'italic #8300ff',
        'i_pink':           'italic #ba1d67',
        'i_red':            'italic #bc2920',
        'i_orange':         'italic #cd620e',
        'i_yellow':         'italic #cac20d',
        'i_grey':           'italic #505050',
        'i_dark_green':     'italic #227547',
        'i_dark_blue':      'italic #2b5893',
        'i_dark_purple':    'italic #542d98',
        'i_dark_pink':      'italic #792f57',
        'i_dark_red':       'italic #712823',
        'i_dark_orange':    'italic #8a5429',
        'i_dark_yellow':    'italic #858125'
    }
    CONSOLE_THEME: ClassVar[Theme] = Theme(COLORS)
    _banner: ClassVar[Any] = None

    def __init__(self) -> None:
        """
        Initialize the instance of Visuals class.

        Attributes:
            console (Console): Instance of rich.Console for handling console output.
        """
        self.console: Console = Console(
            color_system='truecolor', 
            theme=Visuals.CONSOLE_THEME,
            tab_size=6
        )
    
    def banner(
        self,
        name:       Optional[List[str]] = None,
        logo:       Optional[List[str]] = None,
        footern:    Optional[List[str]] = None
    ) -> None:
        """
        Display the banner of the tool
        """
        if isinstance(Visuals._banner, Table):
            self.console.print(Visuals._banner)
            return None

        text_name: Text = Text()
        text_logo: Text = Text()
        text_footern: Text = Text()

        for line in name:
            text_name.append(f'{line}', style=f'{Visuals.COLORS['b_dark_green']}')
        for line in logo:
            text_logo.append(f'{line}', style=f'{Visuals.COLORS['b_dark_blue']}')
        for line in footern:
            text_footern.append(f'{line}', style=f'{Visuals.COLORS['b_dark_purple']}')
        
        table_banner: Table = Table.grid(padding=2)
        table_banner.add_column(no_wrap=2)
        table_banner.add_row(
            Align(text_name, vertical='middle'),
            Align(text_logo, vertical='middle'),
        )
        self.console.print(table_banner)
        self.console.print(text_footern)
    
    def print(
        self, 
        msg:        Union[str, List[str]],
        bad_render: bool = False,
        style:      Optional[str] = None,
        end:        Optional[str] = None,
        start:      str = '',
        type:       Literal['inf', 'war', 'err', 'inp', 'proc', 'list'] = 'inf'
    ) -> None:
        if bad_render: 
            self.special_print(
                msg=msg,
                style=style,
                type=type,
                end=end,
                start=start
            )
            return None

        elif type == 'inf':
            self.console.print(f'{start}[*] {msg}.\n', style='blue', end=end)

        elif type == 'war':
            self.console.print(f'{start}[?] {msg}.\n', style='yellow', end=end)

        elif type == 'err':
            self.console.print(f'{start}[!] {msg}.\n', style='red', end=end)

        elif type == 'inp':
            self.console.print(f'{start}[^] {msg}:', style='green', end=end)

        elif type == 'proc':
            self.console.print(f'{start}[+] {msg}.\n', end=end)

        elif type == 'list':
            if not isinstance(msg, list):
                self.print('Can\'t create list if msg not is array')
                return None
            for content in msg:
                self.console.print(f'{start}\t[-] {content}', style='pink')
            self.console.print()

    def special_print(
        self, 
        msg:    str,
        style:  Optional[str] = None,
        end:    Optional[str] = None,
        start:  str = '',
        type:   Literal['inf', 'war', 'err', 'inp', 'proc', 'list'] = 'proc'
    ) -> None:
        if type == 'inf':
            blue: str = Visuals.COLORS['blue']
            self.console.print(f'{start}[{blue}][*] {msg}.[/{blue}]\n', end=end)

        if type == 'war':
            yellow: str = Visuals.COLORS['yellow']
            self.console.print(f'{start}[{yellow}][?] {msg}.[/{yellow}]\n', end=end)

        if type == 'err':
            red: str = Visuals.COLORS['red']
            self.console.print(f'{start}[{red}][!] {msg}.[/{red}]\n', end=end)

        if type == 'inp':
            green: str = Visuals.COLORS['green']
            self.console.print(f'{start}[{green}][^] {msg}.[/{green}\n', end=end)

        if type == 'proc':
            purple: str = Visuals.COLORS['b_purple']
            self.console.print(f'{start}[{purple}][+] {msg}.[/{purple}]\n', end=end)

        if type == 'list':
            pink: str = Visuals.COLORS['pink']
            if not isinstance(msg, list):
                self.print('Can\'t create list if msg not is array')
                return None
            for content in msg:
                self.console.print(f'{start}\t[{purple}[-] {content}[/{purple}]')
            self.console.print()

    def create_panel(
        self,
        renderable:     Union[RenderableType, Iterable[RenderableType]],
        # title
        title:          Optional[Union[TextType, str]] = None,
        title_align:    Literal['l', 'c', 'r'] = 'c',
        highlight:      bool = False,
        # style
        style:          StyleType = "none",
        # border
        box:            Box = ROUNDED,
        border_style:   StyleType = "none",
        safe_box:       Optional[bool] = None,
        # dimensions
        width:          Optional[int] = None,
        height:         Optional[int] = None,
        expand:         bool = True,
        padding:        PaddingDimensions = (1, 2, 1, 2),
        # subtitle
        subtitle:       Optional[TextType] = None,
        subtitle_align: Literal['l', 'c', 'r']= 'c',
    ) -> Union[Panel, Group]:
        def detect_align(align_type) -> str:
            match title_align:
                case 'l': return 'left'
                case 'c': return 'center'
                case 'r': return 'right'
    
        # management exception when try render Group 'Group object is not iterable'
        try:
            is_panel_grp: bool = all(isinstance(obj, Panel) for obj in renderable)
        except TypeError:
            is_panel_grp: bool = False
    
        # check if its a panel o group of panels
        if is_panel_grp:
            return Group(*renderable)
        return Panel(
            renderable=renderable,
            title=title,
            title_align=detect_align(title_align),
            highlight=highlight,
            style=style,
            box=box,
            border_style=border_style,
            safe_box=safe_box,
            width=width,
            height=height,
            expand=expand,
            padding=padding,
            subtitle=subtitle,
            subtitle_align=detect_align(subtitle_align)
        )
    
    def render_table_db(
        self,
        proc_data:  List[Tuple[Union[str, int, None]]],
        theme:      Literal['cold', 'warm'] = 'cold'
    ) -> None:
        table: Table = Table(
            padding=(0, 1),
            box=DOUBLE_EDGE,
            border_style=f'{Visuals.COLORS['grey']}'
        )

        with Live(table, console=self.console, refresh_per_second=10):
            if not theme == 'cold':
                table.add_column(
                    'Ids', 
                    justify='left', 
                    header_style='b_dark_pink'
                )
                table.add_column(
                    'Sites',
                    justify='left',
                    header_style='b_dark_orange'
                )
                table.add_column(
                    'Usernames',
                    justify='left',
                    header_style='b_dark_yellow'
                )
                table.add_column(
                    'Passwords',
                    justify='left',
                    header_style='b_dark_red'
                )
                table.columns[0].style = f'pink'
                table.columns[1].style = f'orange'
                table.columns[2].style = f'yellow'
                table.columns[3].style = f'red'
            else:
                table.add_column(
                    'Ids', 
                    justify='left', 
                    header_style='b_dark_pink'
                )
                table.add_column(
                    'Sites',
                    justify='left',
                    header_style='b_dark_purple'
                )
                table.add_column(
                    'Usernames',
                    justify='left',
                    header_style='b_dark_blue'
                )
                table.add_column(
                    'Passwords',
                    justify='left',
                    header_style='b_dark_green'
                )
                table.columns[0].style = f'pink'
                table.columns[1].style = f'purple'
                table.columns[2].style = f'blue'
                table.columns[3].style = f'green'
            sleep(0.15)

            # proc and represent row data
            for row_data in proc_data:
                table.add_row(*self._parser_row_data(row_data))
                sleep(0.15)

    def _parser_row_data(self, row_data: List[Union[str, int, None]]) -> List[str]:
        str_row_data: List[str] = []
        for data in row_data:
            if data is not None:
                str_row_data.append(str(data))
                continue
            str_row_data.append(
                f'[{Visuals.COLORS['grey']}]-[/{Visuals.COLORS['grey']}]'
            )
        return str_row_data
