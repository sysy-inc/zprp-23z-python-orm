from typing import Literal
from skibidi_orm.migration_engine.adapters.base_adapter import BaseColumn, BaseTable
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    ForeignKeyConstraint,
    NotNullConstraint,
    PrimaryKeyConstraint,
)
from skibidi_orm.migration_engine.adapters.database_objects.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.revisions.serialization import (
    deserialize_tables,
    serialize_tables,
)


def test_serialize_deserialize_tables_base():
    """Tests whether serializing and deserializing a list of base tables
    yields the original table list"""

    mock_dtypes = Literal["mock_dtype_1", "mock_dtype_2"]
    Column = BaseColumn[mock_dtypes]
    Table = BaseTable[Column]
    test_table_1 = Table(
        "users",
        [
            Column(
                "id",
                "mock_dtype_1",
                [PrimaryKeyConstraint("users", "id"), NotNullConstraint("users", "id")],
            ),
            Column("name", "mock_dtype_2", [NotNullConstraint("users", "name")]),
        ],
    )
    test_table_2 = Table(
        "posts",
        [
            Column(
                "id",
                "mock_dtype_1",
                [PrimaryKeyConstraint("posts", "id"), NotNullConstraint("posts", "id")],
            ),
            Column("content", "mock_dtype_2", [NotNullConstraint("posts", "content")]),
            Column("user_id", "mock_dtype_1"),
        ],
        {ForeignKeyConstraint("posts", "users", {"user_id": "id"})},
    )
    tables = [test_table_1, test_table_2]
    serialized_tables = serialize_tables(tables)
    deserialized_tables = deserialize_tables(serialized_tables)
    assert tables == deserialized_tables


def test_serialize_deserialize_tables_sqlite():
    """Tests whether serializing and deserializing a list of sqlite tables
    yields the original table list"""
    Column = SQLite3Typing.Column
    Table = SQLite3Typing.Table
    test_table_1 = Table(
        "users",
        [
            Column(
                "id",
                "INTEGER",
                [PrimaryKeyConstraint("users", "id"), NotNullConstraint("users", "id")],
            ),
            Column("name", "TEXT", [NotNullConstraint("users", "name")]),
        ],
    )
    test_table_2 = Table(
        "posts",
        [
            Column(
                "id",
                "INTEGER",
                [PrimaryKeyConstraint("posts", "id"), NotNullConstraint("posts", "id")],
            ),
            Column("content", "TEXT", [NotNullConstraint("posts", "content")]),
            Column("user_id", "INTEGER"),
        ],
        {ForeignKeyConstraint("posts", "users", {"user_id": "id"})},
    )
    tables = [test_table_1, test_table_2]
    serialized_tables = serialize_tables(tables)
    deserialized_tables = deserialize_tables(serialized_tables)
    assert tables == deserialized_tables
