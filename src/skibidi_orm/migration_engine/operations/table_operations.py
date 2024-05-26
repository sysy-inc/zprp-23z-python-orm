from __future__ import annotations
from abc import ABC, abstractmethod

from skibidi_orm.exceptions.operations import IrreversibleOperationError
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable, BaseColumn
from typing import Any
from dataclasses import dataclass, field


@dataclass(frozen=True)
class TableOperation(ABC):
    """Base class for table operations"""

    operation_type: OperationType
    table: BaseTable[BaseColumn[Any]]
    is_reversible: bool

    @abstractmethod
    def reverse(self) -> TableOperation:
        """Generates a table operation that reverses
        the calling instance if possible. Else, throws an exception"""


@dataclass(frozen=True)
class CreateTableOperation(TableOperation):
    """Class for creating a table"""

    operation_type: OperationType = field(init=False, default=OperationType.CREATE)
    is_reversible: bool = field(init=False, default=True)

    def reverse(self) -> TableOperation:
        return DeleteTableOperation(table=self.table)

    def __str__(self) -> str:
        return f"Create Table {self.table.name} with columns: {', '.join([col.name for col in self.table.columns])}"


@dataclass(frozen=True)
class DeleteTableOperation(TableOperation):
    """Class for deleting a table"""

    operation_type: OperationType = field(init=False, default=OperationType.DELETE)
    is_reversible: bool = field(init=False, default=False)

    def reverse(self) -> TableOperation:
        raise IrreversibleOperationError(
            f"Reversing a {self.__class__.__name__} is currently not supported."
        )

    def __str__(self) -> str:
        return f"Delete Table {self.table.name}"


@dataclass(frozen=True)
class RenameTableOperation(TableOperation):
    """Class for renaming a table"""

    operation_type: OperationType = field(init=False, default=OperationType.RENAME)
    is_reversible: bool = field(init=False, default=True)
    new_name: str

    def reverse(self) -> TableOperation:
        # todo: make sure it works properly
        return RenameTableOperation(table=self.table, new_name=self.table.name)

    def __str__(self) -> str:
        return f"Rename Table {self.table.name} to {self.new_name}"
