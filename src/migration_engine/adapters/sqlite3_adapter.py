from __future__ import annotations
from typing import Literal
from dataclasses import dataclass, field
from .base_adapter import BaseAdapter


type DataTypes = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
type Constraints = Literal["PRIMARY KEY", "UNIQUE", "NOT NULL", "DEFAULT"]


class SQLite3Adapter(BaseAdapter):

    @dataclass
    class Column:
        """Column dataclass for SQLite3Adapter"""

        name: str
        data_type: DataTypes
        constraints: list[Constraints] = field(default_factory=list)

    @dataclass
    class Table:
        """Table dataclass for SQLite3Adapter"""

        name: str
        columns: list[SQLite3Adapter.Column] = field(default_factory=list)

    tables: list[Table] = []

    def __init__(self):
        pass

    def create_table(self, table: Table):
        """Informs the adapter about Table creation."""

        self.tables.append(table)

    def execute_migration(self):
        """Execute the migration process on a full adapter."""

        for table in self.tables:
            print(f"Creating table {table.name}")
            for column in table.columns:
                print(
                    f"\t Creating column {column.name} with type {column.data_type} and constraints {column.constraints}"
                )


adapter = SQLite3Adapter()

col = adapter.Column("id", "dupa", ["PRIMARY KEY"])
