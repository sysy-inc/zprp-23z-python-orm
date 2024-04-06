from abc import ABC, abstractmethod
from typing import Any

from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseColumn,
    # Relation,
    BaseTable,
)


class BaseDbInspector(ABC):
    @abstractmethod
    def get_tables(self) -> list[BaseTable[BaseColumn[Any, Any]]]:
        pass

    @abstractmethod
    def get_tables_names(self) -> list[str]:
        pass

    @abstractmethod
    def get_table_columns(self, table_name: str) -> list[BaseColumn[Any, Any]]:
        pass

    # @abstractmethod
    # def get_relations(self) -> Relation:
    #     pass
