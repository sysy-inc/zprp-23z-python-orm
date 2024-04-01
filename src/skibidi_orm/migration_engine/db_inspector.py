from abc import ABC, abstractmethod
from typing import Any

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
        x = SQLite3Adapter.Table(
            name="das",
            columns=[
                SQLite3Adapter.Column(
                    name="asd", constraints=["NOT NULL"], data_type="INTEGER"
                )
            ],
        )
        return [x]
