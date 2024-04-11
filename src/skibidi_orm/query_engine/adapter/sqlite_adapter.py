"""
Adapter for SQLite database
"""

from typing import Any
from skibidi_orm.query_engine.adapter.base_adapter import Adapter


class SQLiteAdapter(Adapter):
    """
    Adapter for sqlite database
    """
    def _import_connector(self):
        """
        Import sqlite3, connector for SQLite databse
        """
        # TODO maybe add checking for ImportError
        import sqlite3
        self._connector = sqlite3

    def make_connection(self, **kwargs: dict[str, Any]):
        """
        Creates connection to SQLite database
        :param kwargs: keyword arguments for configuring the database connection
            - path(str): path to sqlite database
        """
        self._import_connector()
        return self._connector.connect(str(kwargs.get('path')))
