from abc import abstractmethod, ABC
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation
from skibidi_orm.migration_engine.operations.table_operations import TableOperation
from skibidi_orm.migration_engine.operations.constraints import Constraint


class SQLConverter(ABC):
    """Class responsible for converting operation and constraint objects
    to raw SQL strings in a specific dialect. Each of the supported database
    providers should inherit a converter from this base class and implement its
    methods"""

    @classmethod
    @abstractmethod
    def convert_table_operation_to_SQL(cls, operation: TableOperation) -> str:
        """Convert a given table operation object to raw SQL in a specific dialect"""

    @classmethod
    @abstractmethod
    def convert_column_operation_to_SQL(cls, operation: ColumnOperation) -> str:
        """Convert a given column operation object to raw SQL in a specific dialect"""

    @classmethod
    @abstractmethod
    def _convert_constraint_to_SQL(cls, constraint: Constraint) -> str:
        """Convert a given constraint to raw SQL in a specific dialect"""
