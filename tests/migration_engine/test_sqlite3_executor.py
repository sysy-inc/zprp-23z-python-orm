from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import SqliteInspector
from skibidi_orm.migration_engine.operations.constraints import (
    PrimaryKeyConstraint,
)
from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor


def test_execute_sql(make_database: str):
    SQLite3Config(make_database)
    SQLite3Executor.execute_sql(
        "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT);"
    )
    table = SqliteInspector().get_tables()[0]
    assert table.name == "test_table"
    assert table.columns[0].name == "id"
    assert table.columns[0].data_type == "INTEGER"
    assert table.columns[0].constraints == [PrimaryKeyConstraint("test_table", "id")]
    assert table.columns[1].name == "name"
    assert table.columns[1].data_type == "TEXT"
    assert table.columns[1].constraints == []
