from abc import ABC, abstractmethod
from skibidi_orm.migration_engine.operations.table_operations import TableOperation
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation


class IStateManager(ABC):
    """
    Interface for the StateManager object. Can be used to calculate changes between class hierarchy schematics and
    database schematics.
    """

    @abstractmethod
    def get_operations_transforming_database_schema_into_class_hierarchy_schema(
        self,
    ) -> list[TableOperation | ColumnOperation]:
        """
        Get operations needed to transform the database structure into a class hierarchy
        defined structure
        """
