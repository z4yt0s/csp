from typing import (
    Self,
    Callable,
    ClassVar,
    Tuple,
    Union,
    Any,
    List,
    Dict
)
from sqlite3 import (
    connect,
    Cursor,
    Connection,
    Error,
    OperationalError
)
from functools import wraps
from os import path
from sys import exc_info

from modules.Crypt import Hasher

# IMPLEMENTS TO FUTURE:
#
# implementar detección de usuario, en el caso de que ya exista
# preguntar al usuario si quiere, eliminarla o pisar la información
# con una respuesta booleana y tal
#
# manejador de errores

class DataManagement:
    """
    DataManagement class handles database operations for the CSP tool

    Attributes:
        _instance (ClassVar[Any]): Stores the single instance of DataManagement.
        _DB_PATH (ClassVar[str]): The path to the SQLite database file.
        _QUERIES (ClassVar[Dict[str, str]]): A dictionary containing predefinied
        SQL queries.
    """
    _instance: ClassVar[Any] = None
    #_DB_PATH: str = '~/.csp/data.db'
    _DB_PATH: ClassVar[str] = './test.db'
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
        INSERT INTO login (site, username, password)
        VALUES ('csp', 'masterkey', ?)
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
        WHERE id != 1 AND id = ?
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
        """
        Implementation of the Singleton pattern for the DataManagement class.
        It ensures that only one instance of this class is created during the
        entire runtime. If an instance already exists, it returns the
        existing instance. If it does not, it creates a new one.

        Args:
            masterkey (str, optional): Master key for database authentication.
            default None.

        Returns:
            Self: Instance of the DataManagement class.
        """
        if cls._instance is not None:
            return cls._instance
        cls._create_database()
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, *args, **kwargs) -> None:
        """
        Initializes a DataManagement instace.

        Atributes:
            conn (Connection): Represents the connection to the SQLite database
            cursor (Cursor): Represents the cursor used to execute SQL queries
        """
        self.conn: Connection = connect(DataManagement._DB_PATH)
        self.cursor: Cursor = self.conn.cursor()

    def handler_err_db(method: Callable) -> Callable:
        """
        Decorator funtion for handling database errors. This catches any exeptions
        that occur during the execution of the decorated method, prints info about
        error, and then either saves and exits if the error is critical or just
        saves if the error is non-critical,

        Args:
            method (Callable): The method to be decorated.

        Returns:
            Callable: The decorated method
        """
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
        """
        Retrieves a predefinied SQL query from the _QUERIES dictionary.

        Args:
            key_query (str): The key of the quey to retrieve.
           
        Returns:
            str: The SQL query string.
        """
        try:
            return cls._QUERIES[key_query]
        except KeyError as ke:
            msg: str = f'[!] The key {key_query} not exist in dictionary _QUERIES'
            raise KeyError(msg) from ke

    @classmethod
    def _create_database(cls) -> Union[bool, None]:
        """
        Create the SQLite database if the doesn't exist and set the master key.

        Args:
            cls: The class object.

        Return: 
            Union[bool, None]: True if the master key already exists in the 
            database, None otherwise.
        """
        try:
            conn: Connection = connect(cls._DB_PATH)
            cursor: Cursor = conn.cursor()
            # create table
            query = cls.predefined_sql('create_tb')
            cursor.execute(query)
        except Error as e:
            print(f'[!] SQLite Err: {e}')
        finally:
            conn.commit()
            conn.close()

    @classmethod
    def masterkey_exists(cls, conn: Connection=None) -> bool:
        """
        Checks if the master key exists in the database.

        Args:
            conn (Connection, optional): An SQLite database connecition.

        Returns:
            bool: True if the master key exists, False otherwise.
        """
        try:
            if conn is None:
                conn: Connection = connect(cls._DB_PATH)
            cursor: Cursor = conn.cursor()
            query: str = cls.predefined_sql('counter_entries')
            cursor.execute(query)
            if cursor.fetchone() != (0,):
                return True
            return False
        except OperationalError as oe:
            print(f'[!] {oe.__class__.__name__}: {oe}')
            return False

    # in future store masterkey in cache so as not to query the db
    @handler_err_db
    def check_master_key(self, masterkey: str) -> bool:
        """
        Checks if the provided master key matches the stored master key in the
        database.

        Args:
            masterkey (str): The master key to check

        Returns:
            bool: True if the master key is correct, False otherwise.
        """
        query: str = DataManagement.predefined_sql('get_masterkey')
        cursor: Cursor = self.cursor.execute(query)
        masterkey_db: Tuple[str] = cursor.fetchone()
        hash_type = Hasher.identify_hash_type(masterkey_db[0])
        if not masterkey_db[0] == hash_type.encrypt(masterkey):
            return False
        return True

    @handler_err_db
    def reset_master_key(self, old_masterkey: str, new_masterkey: str) -> bool:
        """
        Resets the master key to a new value.

        Args:
            old_masterkey (str): The current masterkey stored in database.
            new_masterkey (str): The new master key.

        Returns:
            bool: True if the master key is reset successfully, False otherwise
        """
        if not self.check_master_key(old_masterkey):
            return False
        query: str = DataManagement.predefined_sql('set_masterkey')
        self.cursor.execute(query, (new_masterkey,))
        return True

    @handler_err_db
    def list_data(self, field=None, data_to_find=None) -> List[Tuple[Any]]:
        """
        Retrieve data from the database based on the specified field and data
        to find. If no field or data_to_find is provided, it returns all data
        from the database.

        Args:
            field (str, optional): The field to search for data.
            data_to_find (Any, optional): The data to find in the specified
            field.

        Returns:
            List[Tuple[Any]]: A list of tuples containing the retrieved data.
        """
        if field is not None and data_to_find is not None:
            # trow raise in the future
            #if field not in ['id', 'site', 'username', 'password']:
            #    print(f'[!] The field: {field} its not valid')
            #    return
            tmp_query: str = DataManagement.predefined_sql('get_specific_data')
            query: str = tmp_query.replace('|', field)
            self.cursor.execute(query, (data_to_find,))
        else:
            query: str = DataManagement.predefined_sql('get_data')
            self.cursor.execute(query)
        data: List[Any] = self.cursor.fetchall()
        return data

    @handler_err_db
    def new_entry(self, password: str, site: str=None, username: str=None) -> bool:
        """
        Adds a new entry to the database.

        Args:
            password (str): The password for the new entry.
            site (str, optional): The site name associated with the new entry.
            username (str, optional): The username associated with the new entry.

        Returns:
            bool: True if the new entry is added successfully, False otherwise.
        """
        query: str = DataManagement.predefined_sql('set_data')
        self.cursor.execute(query, (site, username, password,))
        return True

    @handler_err_db
    def update_data(self, field: str, data_upd: str, id: int) -> bool:
        """
        Update the values of a entry to the database.

        Args:
            field (str): name of field of the table
            data_upd (str): data to update or replace.
            id (int): id of registry

        Return:
            bool: True if the new entry is added successfully, False otherwise.
        """
        tmp_query: str = DataManagement.predefined_sql('update_data')
        query: str = tmp_query.replace('|', field)

        self.cursor.execute(query, (data_upd, id,))
        return True

    @handler_err_db
    def delete_data(self, id: int) -> bool:
        """
        Delete data from the database. (Only with the id)

        Args:
            id (int): The ID of the data to delete.

        Returns:
            bool: True if the data is deleted successfully, False otherwise.
        """
        query: str = DataManagement.predefined_sql('drop_data')
        self.cursor.execute(query, (id,))
        return True

    def save_and_exit(self, close_conn: bool=False) -> None:
        """
        Commits changes to the database and closes the connecion.

        Args:
            close_conn (bool, optional): Indicates whether to exit the tool.
        """
        self.conn.commit()
        if close_conn:
            self.conn.close()
