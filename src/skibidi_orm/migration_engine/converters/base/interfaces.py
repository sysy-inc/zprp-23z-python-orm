from __future__ import annotations
from abc import abstractmethod, ABC
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation
from skibidi_orm.migration_engine.operations.table_operations import TableOperation
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    Constraint,
)


class SQLConverter(ABC):
    """Class responsible for converting operation and constraint objects
    to raw SQL strings in a specific dialect. Each of the supported database
    providers should inherit a converter from this base class and implement its
    methods"""

    @staticmethod
    @abstractmethod
    def get_column_operation_converter() -> type[ColumnOperationSQLConverter]:
        """Return the corresponding column operation converter class"""

    @staticmethod
    @abstractmethod
    def get_table_operation_converter() -> type[TableOperationSQLConverter]:
        """Return the corresponsing table operation converter class"""

    @staticmethod
    @abstractmethod
    def get_constraint_converter() -> type[ConstraintSQLConverter]:
        """Return the corresponding constraint converter class"""

    @classmethod
    def convert_table_operation_to_SQL(cls, operation: TableOperation) -> str:
        """Convert a given table operation object to raw SQL in a specific dialect"""
        return cls.get_table_operation_converter().convert_table_operation_to_SQL(
            operation
        )

    @classmethod
    def convert_column_operation_to_SQL(cls, operation: ColumnOperation) -> str:
        """Convert a given column operation object to raw SQL in a specific dialect"""
        return cls.get_column_operation_converter().convert_column_operation_to_SQL(
            operation
        )

    @classmethod
    def _convert_constraint_to_SQL(cls, constraint: Constraint) -> str:
        """Convert a given constraint to raw SQL in a specific dialect"""
        return cls.get_constraint_converter().convert_constraint_to_SQL(constraint)


class ColumnOperationSQLConverter(ABC):
    """Class responsible for converting column operation objects to raw SQL strings
    in a specific dialect. Each of the supported database providers should inherit
    a converter from this base class and implement its methods"""

    @staticmethod
    @abstractmethod
    def convert_column_operation_to_SQL(operation: ColumnOperation) -> str:
        """Convert a given column operation object to raw SQL in a specific dialect"""


class TableOperationSQLConverter(ABC):
    """Class responsible for converting table operation objects to raw SQL strings
    in a specific dialect. Each of the supported database providers should inherit
    a converter from this base class and implement its methods"""

    @staticmethod
    @abstractmethod
    def convert_table_operation_to_SQL(operation: TableOperation) -> str:
        """Convert a given table operation object to raw SQL in a specific dialect"""


class ConstraintSQLConverter(ABC):
    """Class responsible for converting constraint objects to raw SQL strings
    in a specific dialect. Each of the supported database providers should inherit
    a converter from this base class and implement its methods"""

    @staticmethod
    @abstractmethod
    def convert_constraint_to_SQL(constraint: Constraint) -> str:
        """Convert a given constraint object to raw SQL in a specific dialect"""
