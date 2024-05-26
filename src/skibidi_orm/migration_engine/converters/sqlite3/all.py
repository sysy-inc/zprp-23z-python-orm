from skibidi_orm.migration_engine.converters.base.interfaces import (
    ColumnOperationSQLConverter,
    ConstraintSQLConverter,
    SQLConverter,
    SQLQueryConverter,
    TableOperationSQLConverter,
)
from skibidi_orm.migration_engine.converters.sqlite3.columns import (
    SQLite3ColumnOperationConverter,
)
from skibidi_orm.migration_engine.converters.sqlite3.constraints import (
    SQLite3ConstraintConverter,
)
from skibidi_orm.migration_engine.converters.sqlite3.queries import (
    SQLite3QueryConverter,
)
from skibidi_orm.migration_engine.converters.sqlite3.tables import (
    SQLite3TableOperationConverter,
)
from skibidi_orm.migration_engine.revisions.constants import REVISION_TABLE_COLUMN_NAMES
from skibidi_orm.migration_engine.revisions.revision import Revision
from skibidi_orm.migration_engine.adapters.database_objects.sqlite3_typing import (
    SQLite3Typing,
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

    @staticmethod
    def get_query_converter() -> type[SQLQueryConverter]:
        return SQLite3QueryConverter

    @classmethod
    def convert_revision_to_insertion_sql(cls, revision: Revision) -> str:
        revision_table_name = SQLite3Typing.get_revision_table_object().name
        _, timestamp, description, schema_repr, provider, table_data, _ = (
            REVISION_TABLE_COLUMN_NAMES
        )

        return (
            f"INSERT INTO {revision_table_name} "
            f"({', '.join([timestamp, description, schema_repr, provider, table_data])}) VALUES {
                revision.timestamp,
                revision.description,
                revision.schema_repr,
                revision.provider,
                revision.schema_data
            };"
        )
