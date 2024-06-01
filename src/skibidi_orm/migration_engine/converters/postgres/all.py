from skibidi_orm.migration_engine.converters.base.interfaces import (
    ColumnOperationSQLConverter,
    ConstraintSQLConverter,
    SQLConverter,
    TableOperationSQLConverter,
)
from skibidi_orm.migration_engine.converters.postgres.columns import (
    PostgresColumnOperationConverter,
)
from skibidi_orm.migration_engine.converters.postgres.constraints import (
    PostgresConstraintConverter,
)
from skibidi_orm.migration_engine.converters.postgres.tables import (
    PostgresTableOperationConverter,
)


class PostgresConverter(SQLConverter):
    """Class reponsible for converting operation and constraint
    objects to Postgres SQL strings"""

    @staticmethod
    def get_constraint_converter() -> type[ConstraintSQLConverter]:
        return PostgresConstraintConverter

    @staticmethod
    def get_table_operation_converter() -> type[TableOperationSQLConverter]:
        return PostgresTableOperationConverter

    @staticmethod
    def get_column_operation_converter() -> type[ColumnOperationSQLConverter]:
        return PostgresColumnOperationConverter
