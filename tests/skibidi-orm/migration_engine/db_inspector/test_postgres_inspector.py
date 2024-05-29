import pytest
from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig
from skibidi_orm.migration_engine.db_inspectors.postgres_inspector import (
    PostgresInspector,
)
from ..conftest import postgres_db_fixture
from ..sql_data import PostgresTablesData, SQLite3TablesData


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


def test__get_table_columns_names():
    @postgres_db_fixture(
        db_name="postgres",
        db_user="admin",
        db_password="admin",
        db_host="0.0.0.0",
        db_port=5432,
        queries=[PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
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
        columns_names = inspector._get_table_columns_names("table_many_columns1")  # type: ignore
        assert len(columns_names) == 7
        assert sorted(columns_names) == sorted(
            [
                "primary_key",
                "text_not_null",
                "text_nullabe",
                "integer_not_null",
                "integer_nullable",
                "date_not_null",
                "date_nullable",
            ]
        )

    test_fn()


@pytest.mark.parametrize(
    "query, table_name, column_name, expected_data_type",
    [
        (  # 0
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "primary_key",
            "INTEGER",
        ),
        (  # 1
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "text_not_null",
            "TEXT",
        ),
        (  # 2
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "text_nullabe",
            "TEXT",
        ),
        (  # 3
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "integer_not_null",
            "INTEGER",
        ),
        (  # 4
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "integer_nullable",
            "INTEGER",
        ),
        (  # 5
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "date_not_null",
            "DATE",
        ),
        (  # 6
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "date_nullable",
            "DATE",
        ),
        (  # 7
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "big_primary_key_alias",
            "BIGINT",
        ),
        (  # 8
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "bit_varying_alias",
            "BIT VARYING",
        ),
        (  # 9
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "bit_varying_alias_arg",
            "BIT VARYING",
        ),
        (  # 10
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "double_precision",
            "DOUBLE PRECISION",
        ),
        (  # 11
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "timestamp",
            "TIMESTAMP WITHOUT TIME ZONE",
        ),
        (  # 12
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "timestamp_arg",
            "TIMESTAMP WITHOUT TIME ZONE",
        ),
        (  # 13
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "timestamp_without_time_zone",
            "TIMESTAMP WITHOUT TIME ZONE",
        ),
        (  # 14
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "timestamp_without_time_zone_arg",
            "TIMESTAMP WITHOUT TIME ZONE",
        ),
        (  # 15
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "timestamp_with_time_zone_alias",
            "TIMESTAMP WITH TIME ZONE",
        ),
        (  # 16
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "timestamp_with_time_zone_arg_alias",
            "TIMESTAMP WITH TIME ZONE",
        ),
        (  # 17
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "charachter_varying",
            "CHARACTER VARYING",
        ),
        (  # 18
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "charachter_varying_arg",
            "CHARACTER VARYING",
        ),
        (  # 19
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "charachter_varying_alias",
            "CHARACTER VARYING",
        ),
        (  # 20
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            "charachter_varying_alias_args",
            "CHARACTER VARYING",
        ),
    ],
)
def test__get_column_data_type(query, table_name, column_name, expected_data_type):  # type: ignore
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
        data_type = inspector._get_column_data_type(table_name, column_name)  # type: ignore
        assert data_type == expected_data_type

    test_fn()
