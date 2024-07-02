from typing import (
    ClassVar,
    Optional,
    Iterable,
    Tuple,
    List,
    Dict,
)
from pathlib import Path

from prompt_toolkit import PromptSession
from prompt_toolkit.styles import Style
from prompt_toolkit.completion import NestedCompleter
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.cursor_shapes import CursorShape
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.history import InMemoryHistory
from InquirerPy.prompts.list import ListPrompt
from InquirerPy.utils import get_style

from modules.Visuals import Visuals

vs: Visuals = Visuals()

class Prompt:
    _DEF_PROMPT: ClassVar[List[Tuple[str, str]]] = [
        ('class:toolname',  '\ncsp'),
        ('class:symbol',    '> '),
    ]
    _DEF_STYLE: ClassVar[Style] = Style.from_dict({
        # user input
        '':         Visuals.COLORS['grey'],
        # prompt parts
        'msg':      Visuals.COLORS['green'],
        'toolname': Visuals.COLORS['green'],
        'sep':      Visuals.COLORS['pink'],
        'dbname':   Visuals.COLORS['purple'],
        'symbol':   Visuals.COLORS['blue']
    })
    _LIST_STYLE: ClassVar[Dict[str, str]] = {
        'questionmark':         f'fg:{Visuals.COLORS['yellow']}',
        'question':             f'fg:{Visuals.COLORS['yellow']}',
        'answermark':           f'fg:{Visuals.COLORS['green']}',
        'answered_question':    f'fg:{Visuals.COLORS['green']}',
        'answer':               f'fg:{Visuals.COLORS['purple']} bold',
        'pointer':              f'fg:{Visuals.COLORS['orange']} bold',
        'fuzzy_border':         f'fg:{Visuals.COLORS['blue']}',
        'skipped':              f'fg:{Visuals.COLORS['red']}'
    }

    def __init__(self) -> None:
        self.csp_session: PromptSession = self.upd_prompt()

    @classmethod
    def create_tmp_prompt(
        cls,
        msg:        List[Tuple[str, str]],
        password:   Optional[bool] = False,
        style:      Optional[Style] = _DEF_STYLE
    ) -> PromptSession:
        return PromptSession(
            message=msg,
            style=style,
            is_password=password,
            key_bindings=cls._set_tmp_kb(),
            history=InMemoryHistory()
        )

    @classmethod
    def create_list_prompt(
        self,
        message:        str,
        choices:        Iterable,
        style:          Dict[str, str] = _LIST_STYLE,
        qmark:          str = '[?]',
        amark:          str = '[^]',
        mandatory:      bool = False,
        show_cursor:    bool = False,
        border:         bool = True,
        vi_mode:        bool = True,
        keybindings:    Optional[Dict[str, List[Dict[str, str]]]] = {
                            'skip': [{'key': 'c-c'}]
                        },
    ) -> ListPrompt:
        return ListPrompt(
            message=message,
            choices=choices,
            style=get_style(style),
            qmark=qmark,
            amark=amark,
            mandatory=mandatory,
            show_cursor=show_cursor,
            border=border,
            vi_mode=vi_mode,
            keybindings=keybindings
        )

    @classmethod
    def _set_tmp_kb(cls) -> KeyBindings:
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

    def _set_csp_kb(self) -> KeyBindings:
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

    def _set_completer(self) -> NestedCompleter:
        """
        Set the completer for CSP prompt

        Returns
            NestedCompeleter: The configured completer
        """
        return NestedCompleter.from_nested_dict({
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
            'chmk': None,
            'crftp': None,
            'seldb': None,
            'newdb': None,
            'exit': None,
            'help': {
                'list': None,
                'add': None,
                'del': None,
                'upd': None,
                'crftp': None,
                'chmk': None,
            }
        })
    
    def upd_prompt(
        self,
        db_name: Path = '',
        history: Optional[InMemoryHistory] = None
    ) -> PromptSession:
        if db_name:
            message: List[Tuple[str, str]] = [
                ('class:toolname',  '\ncsp'),
                ('class:sep',       ':->'),
                ('class:dbname',    f'[{db_name.name}]'),
                ('class:symbol',    '> '),
            ]
            return PromptSession(
                message=message,
                style=Prompt._DEF_STYLE,
                completer=self._set_completer(),
                complete_style=CompleteStyle.READLINE_LIKE,
                cursor=CursorShape.BEAM,
                key_bindings=self._set_csp_kb(),
                history=history
            )
        return PromptSession(
            message=Prompt._DEF_PROMPT,
            style=Prompt._DEF_STYLE,
            completer=self._set_completer(),
            complete_style=CompleteStyle.READLINE_LIKE,
            cursor=CursorShape.BEAM,
            key_bindings=self._set_csp_kb(),
            history=history
        )
