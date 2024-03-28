from abc import ABC
from skibidi_orm.migration_engine.operations.operation_type import OperationType


class ColumnOperation(ABC):
    """Base class for column operations"""

    isReversible: bool
    operation_type: OperationType


class AddColumn(ColumnOperation):
    """Class for adding a column"""

    operation_type = OperationType.CREATE
    isReversible = True


class DeleteColumn(ColumnOperation):
    """Class for deleting a column"""

    operation_type = OperationType.DELETE
    isReversible = False


class RenameColumn(ColumnOperation):
    """Class for renaming a column"""

    operation_type = OperationType.RENAME
    isReversible = True


class AlterColumn(ColumnOperation):
    """Class for altering a column - changing its type or constraints"""

    operation_type = OperationType.ALTER
    isReversible = True  # TODO: Is this always true with modifying data types?
