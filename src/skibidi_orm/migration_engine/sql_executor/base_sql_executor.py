from abc import ABC, abstractmethod

from skibidi_orm.migration_engine.operations.table_operations import TableOperation
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation


class BaseSQLExecutor(ABC):

    @staticmethod
    @abstractmethod
    def execute_sql(sql: str) -> None:
        """Execute the given SQL query in the database"""
        pass

    @staticmethod
    @abstractmethod
    def execute_operations(operations: list[TableOperation | ColumnOperation]) -> None:
        """Execute the given operations in the database"""
        pass
