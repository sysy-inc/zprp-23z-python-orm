from __future__ import annotations
from typing import Literal
from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseAdapter,
    BaseColumn,
    BaseTable,
)
from skibidi_orm.migration_engine.operations.constraints import (
    ColumnSpecificConstraint,
    ForeignKeyConstraint,
)


class SQLite3Adapter(BaseAdapter):

    DataTypes = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
    ColumnSpecificConstraint = ColumnSpecificConstraint
    ForeignKeyConstraint = ForeignKeyConstraint
    Column = BaseColumn[DataTypes]
    Table = BaseTable[Column]
    tables: list[Table] = []

    def create_table(self, table: Table):
        """Informs the adapter about Table creation."""

        self.tables.append(table)

    def execute_migration(self):
        """Execute the migration process on a full adapter."""

        for table in self.tables:
            print(f"Creating table {table.name}")
            for column in table.columns:
                print(
                    f"\t Creating column {column.name} with type {column.data_type} and constraints {column.column_constraints}"
                )
