from __future__ import annotations
from abc import ABC, abstractmethod
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from dataclasses import dataclass


class TableOperation(ABC):
    """Base class for table operations"""

    operation_type: OperationType
    table_name: str
    is_reversible: bool

    @abstractmethod
    def reverse(self) -> TableOperation:
        """Generates a table operation that reverses
        the calling instance if possible. Else, throws an exception"""


@dataclass(frozen=True)
class CreateTableOperation(TableOperation):
    """Class for creating a table"""

    operation_type = OperationType.CREATE
    is_reversible = True


@dataclass(frozen=True)
class DeleteTableOperation(TableOperation):
    """Class for deleting a table"""

    operation_type = OperationType.DELETE
    is_reversible = False


@dataclass(frozen=True)
class RenameTableOperation(TableOperation):
    """Class for renaming a table"""

    operation_type = OperationType.RENAME
    is_reversible = True
