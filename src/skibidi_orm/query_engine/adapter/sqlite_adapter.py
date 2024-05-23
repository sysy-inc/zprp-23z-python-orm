"""
Adapter for SQLite database
"""

from skibidi_orm.query_engine.adapter.base_adapter import Adapter
from skibidi_orm.query_engine.adapter.sqlite_compiler import SQLiteCompiler


class SQLiteAdapter(Adapter):
    """
    Adapter for sqlite database
    """
    def __init__(self) -> None:
        super().__init__()
        self._compiler = SQLiteCompiler()

    def _import_connector(self):
        """
        Import sqlite3, connector for SQLite databse
        """
        # TODO maybe add checking for ImportError
        import sqlite3
        self._connector = sqlite3

    def make_connection(self, **kwargs: str):
        """
        Creates connection to SQLite database
        :param kwargs: keyword arguments for configuring the database connection
            - path(str): path to sqlite database
        """
        self._import_connector()
        return self._connector.connect(str(kwargs.get('path')))
