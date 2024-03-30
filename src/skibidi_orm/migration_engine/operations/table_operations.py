from abc import ABC
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from dataclasses import dataclass


class TableOperation(ABC):
    """Base class for table operations"""

    operation_type: OperationType
    isReversible: bool


@dataclass(frozen=True)
class CreateTableOperation(TableOperation):
    """Class for creating a table"""

    operation_type = OperationType.CREATE
    isReversible = True


@dataclass(frozen=True)
class DeleteTableOperation(TableOperation):
    """Class for deleting a table"""

    operation_type = OperationType.DELETE
    isReversible = False


@dataclass(frozen=True)
class RenameTableOperation(TableOperation):
    """Class for renaming a table"""

    operation_type = OperationType.RENAME
    isReversible = True
