from typing import (
    ClassVar,
    Dict,
    List
)
from pathlib import Path

from prompt_toolkit import PromptSession
from InquirerPy.prompts.list import ListPrompt

from modules.Visuals import Visuals
from modules.DataManagement import DataManagement
from modules.prompt import Prompt

vs: Visuals = Visuals()

class PathCSP:
    """
    La clase PathCSP se encarga de gestionar y realizar todas las operaciones
    correspondiente a las rutas y ficheros del sistema.
    """
    ROOT_DIR: ClassVar[Path] = Path.home() / '.csp'

    def __init__(self):
        """
        En primer lugar comprueba si existe la ruta de gestion de ficheros, sino
        la crea, posteriormente detecta si existe ficheros .db, en el caso de que
        no se detecten se generara uno con los parametros indicados por el usuario
        """
        if not PathCSP.ROOT_DIR.exists():
            PathCSP.ROOT_DIR.mkdir()
            
        self.db_files: List[Path] = self._upd_list_files()
        if not self.db_files:
            self.create_db_file()
    
    def _upd_list_files(self) -> List[Path]:
        return sorted(PathCSP.ROOT_DIR.glob('**/*.db'))

    def create_db_file(self, arg: str = '') -> None:
        """
        """
        tmp_session: PromptSession = Prompt.create_tmp_prompt(
            msg=[('class:msg', '[^] Specify a name the database file: ')],
        )
        # in future add panel for list existing database files

        while True:
            db_name: str = f'{arg}.db'
            if not arg:
                db_name: str = f'{tmp_session.prompt()}.db'
            db_file: Path = PathCSP.ROOT_DIR / db_name
            if db_file in self.db_files:
                vs.print(
                    f'The file {db_file} already exists, choose another name',
                    type='err',
                    bad_render=True,
                    end='\n'
                )
                arg = ''
                continue
            db_file.touch()
            DataManagement.create_database(db_file)
            break
        self.db_files = self._upd_list_files()

    def select_databases(self) -> Path:
        if len(self.db_files) == 1:
            return self.db_files[0]
        list_prompt: ListPrompt = Prompt.create_list_prompt(
            message='Select database file:',
            choices=[file.name for file in self.db_files]
        )
        path_db: Path = PathCSP.ROOT_DIR / list_prompt.execute()
        return path_db
    
    def drop_database(self) -> None:
        path_db: Path = self.select_databases()
        # TERMINAR MAS TARDE