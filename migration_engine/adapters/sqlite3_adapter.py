from typing import Literal, TypedDict

from adapters.base_adapter import BaseAdapter


class SQLite3Adapter(BaseAdapter):
    type DataTypes = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
    type Constraints = Literal["PRIMARY KEY", "UNIQUE", "NOT NULL", "DEFAULT"]
    Column = TypedDict(
        "Column", {"name": str, "data_type": DataTypes, "constraints": Constraints}
    )
    Table = TypedDict("Table", {"name": str, "columns": list[Column]})
    tables: list[Table] = []

    def __init__(self):
        pass

    def create_table(self, table_name: str, columns: list[Column]):
        self.tables.append({"name": table_name, "columns": columns})

    def execute_migration(self):
        print(self.tables)
        print("Migration executed")
        pass
