from abc import ABC
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from skibidi_orm.migration_engine.operations.constraints import Constraint
from dataclasses import dataclass


class ColumnOperation(ABC):
    """Base class for column operations"""

    isReversible: bool
    operation_type: OperationType
    table_name: str
    column_name: str


@dataclass(frozen=True)
class AddColumn(ColumnOperation):
    """Class for adding a column"""

    operation_type = OperationType.CREATE
    isReversible = True


@dataclass(frozen=True)
class DeleteColumn(ColumnOperation):
    """Class for deleting a column"""

    operation_type = OperationType.DELETE
    isReversible = False


@dataclass(frozen=True)
class RenameColumn(ColumnOperation):
    """Class for renaming a column"""

    operation_type = OperationType.RENAME
    isReversible = True

    new_name: str


@dataclass(frozen=True)
class AddConstraint(ColumnOperation):
    """Class for adding a constraint on a column"""

    operation_type = OperationType.CONSTRAINT_CHANGE
    isReversible = True

    constraint: Constraint


@dataclass(frozen=True)
class DeleteConstraint(ColumnOperation):
    """Class for deleting a constraint on a column"""

    operation_type = OperationType.CONSTRAINT_CHANGE
    isReversible = True

    constraint: Constraint


@dataclass(frozen=True)
class ChangeConstraint(ColumnOperation):
    """Class for changing a constraint on a column"""

    operation_type = OperationType.CONSTRAINT_CHANGE
    isReversible = True

    old_constraint: Constraint
    new_constraint: Constraint


@dataclass(frozen=True)
class ChangeDataType(ColumnOperation):
    """Class for changing the data type of a column"""

    operation_type = OperationType.DTYPE_CHANGE
    isReversible = False
    new_dtype: str
