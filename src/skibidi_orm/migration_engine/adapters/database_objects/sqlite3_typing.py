from typing import Literal
from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseColumn,
    BaseTable,
)

from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    Constraint,
    NotNullConstraint,
)
from skibidi_orm.migration_engine.revisions.constants import (
    REVISION_TABLE_COLUMN_NAMES,
    get_revision_table_name,
)


class SQLite3Typing:

    DataTypes = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
    Constraints = Constraint
    Column = BaseColumn[DataTypes]
    Table = BaseTable[Column]
    tables: list[Table] = []

    @staticmethod
    def get_revision_table_object() -> Table:
        """Get the chumpy table object used to store revision data.
        The table contains the following columns:
            id
            timestamp
            human-readable description
            human-readable schema representation
            configuration data (blob)
            schema data (blob)
        """
        revision_table_name = get_revision_table_name()

        (
            _,
            timestamp,
            description,
            schema_string,
            provider,
            schema_data,
            internal,
        ) = REVISION_TABLE_COLUMN_NAMES

        timestamp_colum = SQLite3Typing.Column(
            name=timestamp,
            data_type="TEXT",
            column_constraints=[NotNullConstraint(revision_table_name, timestamp)],
        )

        description_column = SQLite3Typing.Column(
            name=description,
            data_type="TEXT",
            column_constraints=[NotNullConstraint(revision_table_name, description)],
        )

        schema_string_column = SQLite3Typing.Column(
            name=schema_string,
            data_type="TEXT",
            column_constraints=[NotNullConstraint(revision_table_name, schema_string)],
        )

        provider_column = SQLite3Typing.Column(
            name=provider,
            data_type="TEXT",
            column_constraints=[NotNullConstraint(revision_table_name, provider)],
        )

        schema_data_column = SQLite3Typing.Column(
            name=schema_data,
            data_type="BLOB",
            column_constraints=[NotNullConstraint(revision_table_name, schema_data)],
        )

        internal_special_column = SQLite3Typing.Column(
            name=internal,
            data_type="TEXT",
        )

        revision_table_columns = [
            timestamp_colum,
            description_column,
            schema_string_column,
            provider_column,
            schema_data_column,
            internal_special_column,
        ]

        return SQLite3Typing.Table(
            name=revision_table_name,
            columns=revision_table_columns,
        )
