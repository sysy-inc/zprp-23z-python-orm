from __future__ import annotations
from abc import abstractmethod, ABC
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation
from skibidi_orm.migration_engine.operations.table_operations import (
    TableOperation,
)
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

    @classmethod
    def convert_operation_to_SQL(
        cls, operation: ColumnOperation | TableOperation
    ) -> str:
        """Convert a given operation object to raw SQL in a specific dialect"""
        if isinstance(operation, ColumnOperation):
            return cls.get_column_operation_converter().convert_column_operation_to_SQL(
                operation
            )
        return cls.get_table_operation_converter().convert_table_operation_to_SQL(
            operation
        )

    @staticmethod
    @abstractmethod
    def get_query_converter() -> type[SQLQueryConverter]:
        """Return the corresponding query converter class"""

    @classmethod
    def get_revision_table_creation_query(cls) -> str:
        """Return the SQL string which creates a special internal table
        used to hold revision data"""
        return cls.get_table_operation_converter().get_revision_table_creation_query()

    @classmethod
    @abstractmethod
    def get_table_clearing_query(cls) -> str:
        """Return the SQL string which clears the table of all data
        except the revision table"""
        return cls.get_query_converter().get_table_clearing_query()

    @classmethod
    @abstractmethod
    def get_revision_insertion_query(cls) -> str:
        """Return the SQL string which inserts a revision into the revision table.
        The revision needs to be provided as a second argument to cur.execute()"""

    @classmethod
    def get_revision_data_query(cls) -> str:
        """Return the SQL string which selects all of the data from the revision table"""
        return cls.get_query_converter().get_revision_data_query()


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

    @staticmethod
    @abstractmethod
    def get_revision_table_creation_query() -> str:
        """Return the SQL string which creates a special internal table
        used to hold revision data"""


class ConstraintSQLConverter(ABC):
    """Class responsible for converting constraint objects to raw SQL strings
    in a specific dialect. Each of the supported database providers should inherit
    a converter from this base class and implement its methods"""

    @staticmethod
    @abstractmethod
    def convert_constraint_to_SQL(constraint: Constraint) -> str:
        """Convert a given constraint object to raw SQL in a specific dialect"""


class SQLQueryConverter(ABC):
    """Class responsible for converting SELECT queries to raw SQL strings.
    Used mainly to retrieve data from the revision table."""

    @staticmethod
    @abstractmethod
    def get_revision_data_query() -> str:
        """Return the SQL string which selects all of the data from the revision table"""

    @staticmethod
    @abstractmethod
    def get_table_clearing_query() -> str:
        """Return the SQL string which clears the table of all data
        except the revision table"""
