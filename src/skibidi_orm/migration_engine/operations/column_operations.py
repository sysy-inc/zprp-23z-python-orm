from __future__ import annotations
from abc import ABC, abstractmethod
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from skibidi_orm.migration_engine.operations.constraints import Constraint
from skibidi_orm.exceptions.irreversible_operation import IrreversibleOperationError
from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable, BaseColumn
from typing import Any
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ColumnOperation(ABC):
    """Base class for column operations"""

    is_reversible: bool = field(init=False)
    operation_type: OperationType = field(init=False)
    table: BaseTable[BaseColumn[Any]]
    column: BaseColumn[Any]

    @abstractmethod
    def reverse(self) -> ColumnOperation:
        """Generates a table operation that reverses
        the calling instance if possible. Else, throws an exception"""


@dataclass(frozen=True)
class AddColumnOperation(ColumnOperation):
    """Class for adding a column"""

    operation_type: OperationType = field(init=False, default=OperationType.CREATE)
    is_reversible: bool = field(init=False, default=True)

    def reverse(self) -> ColumnOperation:
        return DeleteColumnOperation(table=self.table, column=self.column)


@dataclass(frozen=True)
class DeleteColumnOperation(ColumnOperation):
    """Class for deleting a column"""

    operation_type: OperationType = field(init=False, default=OperationType.DELETE)
    is_reversible: bool = field(init=False, default=False)

    def reverse(self) -> ColumnOperation:
        raise IrreversibleOperationError(
            f"Reversing a {self.__class__.__name__} is currently not supported."
        )


@dataclass(frozen=True)
class RenameColumnOperation(ColumnOperation):
    """Class for renaming a column"""

    operation_type: OperationType = field(init=False, default=OperationType.RENAME)
    is_reversible: bool = field(init=False, default=True)

    new_name: str

    def reverse(self) -> ColumnOperation:
        return RenameColumnOperation(
            table=self.table,
            column=self.column,
            new_name=self.column.name,
        )


@dataclass(frozen=True)
class AddConstraintOperation(ColumnOperation):
    """Class for adding a constraint on a column"""

    operation_type: OperationType = field(
        init=False, default=OperationType.CONSTRAINT_CHANGE
    )
    is_reversible: bool = field(init=False, default=True)

    constraint: Constraint

    def reverse(self) -> ColumnOperation:
        return DeleteConstraintOperation(
            table=self.table,
            column=self.column,
            constraint=self.constraint,
        )


@dataclass(frozen=True)
class DeleteConstraintOperation(ColumnOperation):
    """Class for deleting a constraint on a column"""

    operation_type: OperationType = field(
        init=False, default=OperationType.CONSTRAINT_CHANGE
    )
    is_reversible: bool = field(init=False, default=True)

    constraint: Constraint

    def reverse(self) -> ColumnOperation:
        return AddConstraintOperation(
            table=self.table,
            column=self.column,
            constraint=self.constraint,
        )


@dataclass(frozen=True)
class ChangeDataTypeOperation(ColumnOperation):
    """Class for changing the data type of a column"""

    operation_type: OperationType = field(
        init=False, default=OperationType.DTYPE_CHANGE
    )
    is_reversible: bool = field(init=False, default=True)
    new_dtype: str

    def reverse(self) -> ColumnOperation:
        return ChangeDataTypeOperation(
            table=self.table,
            column=self.column,
            new_dtype=self.column.data_type,
        )
