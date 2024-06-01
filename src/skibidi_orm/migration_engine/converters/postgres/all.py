from skibidi_orm.migration_engine.converters.base.interfaces import (
    ColumnOperationSQLConverter,
    ConstraintSQLConverter,
    SQLConverter,
    TableOperationSQLConverter,
)
from skibidi_orm.migration_engine.converters.sqlite3.columns import (
    SQLite3ColumnOperationConverter,
)
from skibidi_orm.migration_engine.converters.sqlite3.constraints import (
    SQLite3ConstraintConverter,
)
from skibidi_orm.migration_engine.converters.sqlite3.tables import (
    SQLite3TableOperationConverter,
)


class SQLite3Converter(SQLConverter):
    """Class reponsible for converting operation and constraint
    objects to SQLite3 SQL strings"""

    @staticmethod
    def get_constraint_converter() -> type[ConstraintSQLConverter]:
        return SQLite3ConstraintConverter

    @staticmethod
    def get_table_operation_converter() -> type[TableOperationSQLConverter]:
        return SQLite3TableOperationConverter

    @staticmethod
    def get_column_operation_converter() -> type[ColumnOperationSQLConverter]:
        return SQLite3ColumnOperationConverter
