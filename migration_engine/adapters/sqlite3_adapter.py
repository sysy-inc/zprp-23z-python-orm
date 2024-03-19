from __future__ import annotations
from typing import Literal, TypedDict
from dataclasses import dataclass
from adapters.base_adapter import BaseAdapter


type DataTypes = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
type Constraints = Literal["PRIMARY KEY", "UNIQUE", "NOT NULL", "DEFAULT"]


@dataclass
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
