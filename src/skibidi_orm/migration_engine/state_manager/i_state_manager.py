from abc import ABC, abstractmethod
from skibidi_orm.migration_engine.operations.table_operations import TableOperation
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation


class IStateManager(ABC):

    @abstractmethod
    def get_operations(self) -> list[TableOperation | ColumnOperation]:
        """Get operations needed to transform database structure into schema structure"""
