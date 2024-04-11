from skibidi_orm.migration_engine.adapters.sqlite3_converter import SQLite3Converter
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.operations.table_operations import (
    CreateTableOperation,
    DeleteTableOperation,
    RenameTableOperation,
)


simple_table = SQLite3Adapter.Table(
    "users", columns=[SQLite3Adapter.Column("name", "TEXT")]
)


def test_add_column_conversion_simple():
    """Create a simple table"""
    operation = CreateTableOperation(simple_table)
    assert (
        SQLite3Converter.convert_table_operation_to_SQL(operation)
        == "CREATE TABLE users (name TEXT);"
    )


def test_delete_table_conversion_simple():
    """Delete a simple table"""
    operation = DeleteTableOperation(simple_table)
    assert (
        SQLite3Converter.convert_table_operation_to_SQL(operation)
        == "DROP TABLE users;"
    )


def test_rename_table_conversion_simple():
    """Rename a table"""
    operation = RenameTableOperation(simple_table, "users2")
    assert (
        SQLite3Converter.convert_table_operation_to_SQL(operation)
        == "DROP TABLE users; CREATE TABLE users2 (name TEXT);"
    )
