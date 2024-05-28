from __future__ import annotations
from abc import ABC, abstractmethod
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    Constraint,
    ForeignKeyConstraint,
)
from skibidi_orm.exceptions.operations import IrreversibleOperationError
from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable, BaseColumn
from typing import Any
from dataclasses import dataclass, field
from typing import Optional


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

    def get_related_foreign_keys(self) -> list[ForeignKeyConstraint]:
        """Returns the foreign keys that are related to the column operation.
        If the column is already instantiated and is a part of a foreign key,
        it has to be taken into acount when removing and adding it back to the schema.
        """
        return [
            fk
            for fk in self.table.foreign_keys
            if self.column.name in fk.column_mapping
        ]


@dataclass(frozen=True)
class AddColumnOperation(ColumnOperation):
    """Class for adding a column"""

    operation_type: OperationType = field(init=False, default=OperationType.CREATE)
    is_reversible: bool = field(init=False, default=True)

    # if the column to be added references another table, it has to be set here
    related_foreign_key: Optional[ForeignKeyConstraint] = field(default=None)

    def reverse(self) -> ColumnOperation:
        return DeleteColumnOperation(table=self.table, column=self.column)

    def __post_init__(self):
        self.validate_related_foreign_key()

    def validate_related_foreign_key(self) -> None:
        """This method validates the related_foreign_key attribute of the AddColumnOperation.
        The field is supposed to serve as a way to add a non-composite foreign key to the table
        as a column is being added. Trying to add a composite foreign key or one that does not have
        the added column as the origin column will result in an error."""
        if self.related_foreign_key is not None:
            if len(self.related_foreign_key.column_mapping.values()) != 1:
                raise ValueError(
                    "The related_foreign_key should have exactly one column mapping, with the key being the column that's added to the table"
                )
            if self.column.name not in self.related_foreign_key.column_mapping:
                raise ValueError(
                    "The only possible key value for the column mapping in an AddColumnOperation is the added column name"
                )
            if self.table.name != self.related_foreign_key.table_name:
                raise ValueError(
                    f"""Foreign key constraint initialized with invalid source table name: {self.related_foreign_key.table_name}.
                    Expected: {self.table.name}"""
                )
    def __str__(self) -> str:
        return f"Add Column {self.column.name} to Table {self.table.name}"

@dataclass(frozen=True)
class DeleteColumnOperation(ColumnOperation):
    """Class for deleting a column"""

    operation_type: OperationType = field(init=False, default=OperationType.DELETE)
    is_reversible: bool = field(init=False, default=False)

    def reverse(self) -> ColumnOperation:
        raise IrreversibleOperationError(
            f"Reversing a {self.__class__.__name__} is currently not supported."
        )

    def __str__(self) -> str:
        return f"Delete Column {self.column.name} from Table {self.table.name}"


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

    def __str__(self) -> str:
        return f"Rename Column {self.column.name} to {self.new_name} in Table {self.table.name}"


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

    def __str__(self) -> str:
        return f"Add Constraint {self.constraint.constraint_type.value} to Column {self.column.name} in Table {self.table.name}"


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

    def __str__(self) -> str:
        return f"Delete Constraint {self.constraint.constraint_type.value} from Column {self.column.name} in Table {self.table.name}"


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

    def __str__(self) -> str:
        return f"Change Data Type of Column {self.column.name} in Table {self.table.name} to {self.new_dtype}"
