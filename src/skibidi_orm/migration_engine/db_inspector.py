from abc import ABC, abstractmethod
from typing import Any
import sqlite3

from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseColumn,
    BaseTable,
)
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.config import SQLite3Config


class DbInspector(ABC):
    @abstractmethod
    def get_tables(self) -> list[BaseTable[BaseColumn[Any, Any]]]:
        pass


class SqliteInspector(DbInspector):
    """
    Used to get data from live SQLite3 database.
    Should only be instantiated when SQLite3 is choosen as the database.
    """

    def __init__(self) -> None:
        self.config = SQLite3Config.instance()

    def get_tables(
        self,
    ) -> list[
        BaseTable[BaseColumn[SQLite3Adapter.DataTypes, SQLite3Adapter.Constraints]]
    ]:
        tables_names = self.get_tables_names()

        return [BaseTable(name=table[0]) for table in tables_names]

    def get_tables_names(self) -> list[str]:
        db_path = self.config.db_path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        cursor.close()
        conn.close()
        return [table[0] for table in tables]
