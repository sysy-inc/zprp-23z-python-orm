from typing import Literal, TypedDict

from base_adapter import BaseAdapter


class SQLite3Adapter(BaseAdapter):
    type DataTypes = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
    type Constraints = Literal["PRIMARY KEY", "UNIQUE", "NOT NULL", "DEFAULT"]
    Column = TypedDict(
        "Column", {"name": str, "data_type": DataTypes, "constraints": Constraints}
    )

    def __init__(self):
        pass

    def create_table(self, table_name: str, columns: list[Column]):
        pass
