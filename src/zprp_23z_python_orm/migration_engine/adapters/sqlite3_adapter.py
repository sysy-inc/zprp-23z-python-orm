from __future__ import annotations
from typing import List, Literal, TypedDict
from dataclasses import dataclass
from zprp_23z_python_orm.migration_engine.adapters.base_adapter import BaseAdapter


type DataTypes = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
type Constraints = Literal["PRIMARY KEY", "UNIQUE", "NOT NULL", "DEFAULT"]


class SQLite3Adapter(BaseAdapter):

    @dataclass
    class Column:
        name: str
        data_type: DataTypes
        constraints: list[Constraints]

    @dataclass
    class Table:
        name: str
        columns: list[SQLite3Adapter.Column]

    tables: list[Table] = []

    def __init__(self):
        pass

    def create_table(self, table: Table):
        self.tables.append(table)

    def execute_migration(self):
        return super().execute_migration()
