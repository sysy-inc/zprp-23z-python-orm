from abc import ABC, abstractmethod
from typing import Any

from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseColumn,
    BaseTable,
)
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter


class DbInspector(ABC):
    @abstractmethod
    def get_tables(self) -> list[BaseTable[BaseColumn[Any, Any]]]:
        pass


class SqliteInspector(DbInspector):
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
