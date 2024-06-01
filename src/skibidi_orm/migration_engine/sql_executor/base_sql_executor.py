from abc import ABC, abstractmethod
from typing import Any

from skibidi_orm.migration_engine.operations.table_operations import TableOperation
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation
from skibidi_orm.migration_engine.revisions.revision import Revision


class BaseSQLExecutor(ABC):

    @staticmethod
    @abstractmethod
    def execute_sql(sql: str) -> None:
        """Execute the given SQL query in the database"""

    @staticmethod
    @abstractmethod
    def execute_sql_query(sql: str) -> list[Any]:
        """Execute the given SQL query in the database and
        return its result"""

    @staticmethod
    @abstractmethod
    def execute_operations(operations: list[TableOperation | ColumnOperation]) -> None:
        """Execute the given operations in the database"""

    @staticmethod
    @abstractmethod
    def save_revision(revision: Revision) -> None:
        """Save the given revision in the database"""

    @staticmethod
    @abstractmethod
    def get_all_revisions() -> list[tuple[int, Revision]]:
        """Get all the revisions from the database
        returns a list of tuples (id, revision)"""
