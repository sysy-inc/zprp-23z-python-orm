from abc import ABC, abstractmethod
from typing import Any, Literal, cast
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


type PragmaTableInfo = list[tuple[int, str, str, Literal[0, 1], Any, Literal[0, 1]]]


class SqliteInspector(DbInspector):
    """
    Used to get data from live SQLite3 database.
    Should only be instantiated when SQLite3 is choosen as the database.
    """

    def __init__(self) -> None:
        self.config = SQLite3Config.instance()

    def get_tables(
        self,
    ) -> list[SQLite3Adapter.Table]:
        tables: list[SQLite3Adapter.Table] = []
        tables_names = self.get_tables_names()
        for table_name in tables_names:
            table_columns = self.get_table_columns(table_name)
            tables.append(SQLite3Adapter.Table(name=table_name, columns=table_columns))

        return tables

    def get_tables_names(self) -> list[str]:
        tables = self._sqlite_execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        return [table[0] for table in tables]

    def get_table_columns(self, table_name: str) -> list[SQLite3Adapter.Column]:
        columns: PragmaTableInfo = self._sqlite_execute(
            f"PRAGMA table_info({table_name});"
        )
        adapter_columns: list[SQLite3Adapter.Column] = []

        for _, name, data_type, notnull, _, pk in columns:
            constraints: list[SQLite3Adapter.Constraints] = []
            if pk:
                constraints.append("PRIMARY KEY")
            if notnull:
                constraints.append("NOT NULL")

            adapter_columns.append(
                SQLite3Adapter.Column(
                    name=name,
                    data_type=cast(SQLite3Adapter.DataTypes, data_type),
                    constraints=constraints,
                )
            )

        return adapter_columns

    def _sqlite_execute(self, query: str):
        db_path = self.config.db_path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(query)
        conn.commit()
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data
