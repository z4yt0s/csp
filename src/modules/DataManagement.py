from typing import Self, Any, List, Dict, NoReturn, Union, ClassVar
from functools import wraps
from os import path
from sys import exc_info
from sqlite3 import (
    connect,
    Cursor,
    Connection,
    Error,
    OperationalError
)
# IMPLEMENTS TO FUTURE:
#
# implementar detección de usuario, en el caso de que ya exista
# preguntar al usuario si quiere, eliminarla o pisar la información
# con una respuesta booleana y tal
#
# manejador de errores

class DataManagement:
    _instance = None
    #_DB_PATH: str = '~/.csp/data.db'
    _DB_PATH: ClassVar[str] = '../test.db'
    _QUERIES: ClassVar[Dict[str, str]] = {
    'create_tb': '''
        CREATE TABLE IF NOT EXISTS login (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            site TEXT,
            username TEXT,
            password TEXT REQUIRED
        )
    ''',
    'set_masterkey': '''
        INSERT INTO login (username, password)
        VALUES ('masterkey', ?)
    ''',
    'set_data': '''
        INSERT INTO login (site, username, password)
        VALUES (?, ?, ?)
    ''',
    'get_masterkey': '''
        SELECT password FROM login
        WHERE id = 1
    ''',
    'get_data': '''
        SELECT * FROM login
        WHERE id != 1
    ''',
    #'get_specific_data': 'SELECT password FROM login WHERE | = ? AND id != 1',
    'get_specific_data': '''
        SELECT * FROM login
        WHERE id != 1 AND | = ?
    ''',
    'update_masterkey': '''
        UPDATE login SET password = ?
        WHERE id = 1
    ''',
    'update_data': '''
        UPDATE login SET | = ?
        WHERE id != 1 AND | = ?
    ''',
    'drop_data': '''
        DELETE FROM login 
        WHERE id != 1 and id = ?
    ''',
    'counter_entries': '''
        SELECT COUNT(*) FROM login
    '''
    }

    def __new__(cls, masterkey: str = None, *args, **kwargs) -> Self:
        if cls._instance is not None:
            return cls._instance
        cls._create_database(masterkey)
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs) -> None:
        self.conn: Connection = connect(DataManagement._DB_PATH)
        self.cursor: Cursor = self.conn.cursor()

    def handler_err_db(method):
        @wraps(method)
        def wrapper(self_cls, *args, **kwargs):
            try:
                return method(self_cls, *args, **kwargs)
            except Error as e:
                # Operational Error: (list_data)
                    # no such column user
                    # incomplete input
                    # unrecognized token
                # Programming Error: (list_data)
                    # yo can only execute one statement at time
                print({e.__class__})
                print(f'(|{method.__name__}|" Error de SQLite: {e}')
            finally:
                # exc_info() -> Tuple(type_exc, val_exc, tracebakc_exc)
                type_exc: BaseException
                type_exc, _, _ = exc_info()
                if type_exc is not None:
                    self_cls.save_and_exit(True)
                else:
                    self_cls.save_and_exit()
        return wrapper

    @classmethod
    def predefined_sql(cls, key_query: str) -> str:
        try:
            return cls._QUERIES[key_query]
        except KeyError as ke:
            msg: str = f'[!] The key {key_query} not exist in dictionary _QUERIES'
            raise KeyError(msg) from ke

    @classmethod
    def _create_database(cls, masterkey) -> None:
        try:
            conn: Connection = connect(cls._DB_PATH)
            cursor: Cursor = conn.cursor()
            # create table
            query = cls.predefined_sql('create_tb')
            cursor.execute(query)
            # check if exists masterkey
            if cls.masterkey_exists(conn):
                return 
            # insert masterkey
            query = cls.predefined_sql('set_masterkey')
            cursor.execute(query, (masterkey,))
            print('[primera masterkey insertada]')
        except Error as e:
            print(f'[!] SQLite Err: {e}')
        finally:
            conn.commit()
            conn.close()
    
    @classmethod
    def masterkey_exists(cls, conn: Connection=None) -> bool: #Union[bool, OperationalError]:
        try:
            if conn is None:
                conn: Connection = connect(cls._DB_PATH)
            cursor: Cursor = conn.cursor()
            query = cls.predefined_sql('counter_entries')
            cursor.execute(query)
            if cursor.fetchone() != (0,):
                return True
            return False
        except OperationalError as oe:
            print(f'[!] {oe.__class__.__name__}: {oe}')
            return False
            #return oe

    # in future store masterkey in cache so as not to query the db
    @handler_err_db
    def check_master_key(self, masterkey: str) -> bool:
        query: str = DataManagement.predefined_sql('get_masterkey')
        cursor: Cursor = self.cursor.execute(query)
        masterkey_db: str = cursor.fetchone()
        # in future implement decript masterkey
        if not masterkey_db[0] == masterkey:
            return False
        return True
        
    @handler_err_db
    def reset_master_key(self, old_masterkey: str, new_masterkey: str) -> bool:
        if not self.check_master_key(old_masterkey):
            return False
        query: str = DataManagement.predefined_sql('set_masterkey')
        self.cursor.execute(query, (new_masterkey,))
        return True

    @handler_err_db
    def list_data(self, field=None, data_to_find=None) -> List[Any]:
        if field is not None and data_to_find is not None:
            # trow raise in the future
            #if field not in ['id', 'site', 'username', 'password']:
            #    print(f'[!] The field: {field} its not valid')
            #    return
            tmp_query: str = DataManagement.predefined_sql('get_specific_data')
            query = tmp_query.replace('|', field)
            self.cursor.execute(query, (data_to_find,))
        else:
            query: str = DataManagement.predefined_sql('get_data')
            self.cursor.execute(query)
        data: List[Any] = self.cursor.fetchall()
        return data

    @handler_err_db
    def new_entry(self, password: str, site: str=None, username: str=None) -> bool:
        query: str = DataManagement.predefined_sql('set_data')
        self.cursor.execute(query, (site, username, password,))
        return True

    @handler_err_db
    def delete_data(self, id: int) -> bool:
        query: str = DataManagement.predefined_sql('delete_data')
        self.cursor.execute(query, (id,))
        return True
    
    def save_and_exit(self, exit: bool = False):
        self.conn.commit()
        if exit:
            self.conn.close()
