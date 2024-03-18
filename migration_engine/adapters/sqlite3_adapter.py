from typing import Literal

from base_adapter import BaseAdapter


class SQLite3Adapter(BaseAdapter):
    type data_types = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
    type constraints = Literal["PRIMARY KEY", "UNIQUE", "NOT NULL", "DEFAULT"]

    def __init__(self):
        pass

    def create_table(self, table_name: str, columns):
        return super().create_table(table_name, columns)


SQLite3Adapter()
print("x")
