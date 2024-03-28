from abc import ABC
from skibidi_orm.migration_engine.operations.operation_type import OperationType


class TableOperation(ABC):
    """Base class for table operations"""

    operation_type: OperationType
    isReversible: bool


class CreateTable(TableOperation):
    """Class for creating a table"""

    operation_type = OperationType.CREATE
    isReversible = True


class DeleteTable(TableOperation):
    """Class for deleting a table"""

    operation_type = OperationType.DELETE
    isReversible = False


class RenameTable(TableOperation):
    """Class for renaming a table"""

    operation_type = OperationType.RENAME
    isReversible = True


class AlterTable(TableOperation):
    """Class for altering a table - adding or removing columns"""

    operation_type = OperationType.ALTER
    isReversible = True
