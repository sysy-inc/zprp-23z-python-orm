from abc import ABC, abstractmethod
from typing import Any

from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseColumn,
    BaseTable,
)


class BaseDbInspector(ABC):
    @abstractmethod
    def get_tables(self) -> list[BaseTable[BaseColumn[Any]]]:
        """
        Get all tables from the database.
        """
        pass

    @abstractmethod
    def get_tables_names(self) -> list[str]:
        """
        Get all tables names from the database.
        """
        pass

    @abstractmethod
    def get_table_columns(self, table_name: str) -> list[BaseColumn[Any]]:
        """
        Get all columns from a table.
        """
        pass
