from __future__ import annotations
from typing import Literal
from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseAdapter,
    BaseColumn,
    Relation,
    BaseTable,
)


class SQLite3Adapter(BaseAdapter):

    DataTypes = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
    Constraints = Literal["PRIMARY KEY", "UNIQUE", "NOT NULL", "DEFAULT"]
    Column = BaseColumn[DataTypes, Constraints]
    Table = BaseTable[Column]

    tables: list[Table] = []
    relations: list[Relation] = []

    def __init__(self):
        pass

    def create_table(self, table: Table):
        """Informs the adapter about Table creation."""

        self.tables.append(table)

    def create_relation(
        self,
        relation: Relation,
    ):
        """Informs the adapter about a relation creation."""

        self.relations.append(relation)
        print(
            f"Creating relation from {relation.origin_table}.{relation.origin_column} to {relation.referenced_table}.{relation.referenced_column}"
        )

    def execute_migration(self):
        """Execute the migration process on a full adapter."""

        for table in self.tables:
            print(f"Creating table {table.name}")
            for column in table.columns:
                print(
                    f"\t Creating column {column.name} with type {column.data_type} and constraints {column.constraints}"
                )
