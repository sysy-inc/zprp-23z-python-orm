import pytest
from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig
from skibidi_orm.migration_engine.db_inspectors.postgres_inspector import (
    PostgresInspector,
)
from ..conftest import postgres_db_fixture
from ..sql_data import SQLite3TablesData


@pytest.mark.parametrize(
    "query, expected_tables_len, expected_tables_list",
    [
        ([SQLite3TablesData.sql_table1], 1, ["table1"]),
        (
            [SQLite3TablesData.sql_table1, SQLite3TablesData.sql_table2],
            2,
            ["table1", "table2"],
        ),
        (
            [SQLite3TablesData.sql_table_primary_key_not_null],
            1,
            ["table_primary_key_not_null"],
        ),
    ],
)
def test_get_tables_names(query, expected_tables_list, expected_tables_len):  # type: ignore
    @postgres_db_fixture(
        db_name="postgres",
        db_user="admin",
        db_password="admin",
        db_host="0.0.0.0",
        db_port=5432,
        queries=query,  # type: ignore
    )
    def test_fn():
        PostgresConfig(
            db_name="postgres",
            db_user="admin",
            db_password="admin",
            db_host="0.0.0.0",
            db_port=5432,
        )
        inspector = PostgresInspector()
        tables = inspector.get_tables_names()
        assert len(tables) == expected_tables_len
        assert sorted(expected_tables_list) == sorted(tables)  # type: ignore

    test_fn()
