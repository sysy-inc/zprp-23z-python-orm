from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite.sqlite3_inspector import (
    SQLite3Inspector,
)
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    PrimaryKeyConstraint,
)
from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor

type TestTableRow = tuple[int, str | None]


def test_execute_sql(make_database: str):
    SQLite3Config(make_database)
    SQLite3Executor.execute_sql(
        "CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT);"
    )
    table = SQLite3Inspector().get_tables()[0]
    assert table.name == "test_table"
    assert table.columns[0].name == "id"
    assert table.columns[0].data_type == "INTEGER"
    assert table.columns[0].column_constraints == [
        PrimaryKeyConstraint("test_table", "id")
    ]
    assert table.columns[1].name == "name"
    assert table.columns[1].data_type == "TEXT"
    assert table.columns[1].column_constraints == []


def test_execute_query(make_database: str):
    SQLite3Config(make_database)
    SQLite3Executor.execute_sql(
        """
        CREATE TABLE test_table (id INTEGER PRIMARY KEY, name TEXT);
        INSERT INTO test_table (id, name) VALUES (1, 'test1');
        INSERT INTO test_table (id) VALUES (2);
        """
    )
    table_contents: list[TestTableRow] = SQLite3Executor.execute_sql_query(
        "SELECT * FROM test_table;"
    )

    assert table_contents == [(1, "test1"), (2, None)]
