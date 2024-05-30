"""
Adapter for SQLite database
"""

from skibidi_orm.query_engine.adapter.base_adapter import Adapter
from skibidi_orm.query_engine.adapter.sqlite_compiler import SQLiteCompiler


class SQLiteAdapter(Adapter):
    """
    Adapter for SQLite database
    """
    def __init__(self) -> None:
        """
        Initializes an SQLiteAdapter instance.

        Sets up the SQLite-specific SQL compiler.
        """
        super().__init__()
        self._compiler = SQLiteCompiler()

    def _import_connector(self):
        """
        Imports sqlite3, the connector for SQLite databases.
        """
        import sqlite3
        self._connector = sqlite3

    def make_connection(self, **kwargs: str):
        """
        Creates a connection to the SQLite database.

        Args:
            **kwargs: Keyword arguments for configuring the database connection.
                - path (str): Path to the SQLite database.

        Returns:
            sqlite3.Connection: A connection object to the SQLite database.

        Examples:
            make_connection(path="database.db")
        """
        self._import_connector()
        return self._connector.connect(str(kwargs.get('path')))
