"""
Notice about postgres constraints and types:

1. SERIAL/BIGSERIAL:
    - expands to INTEGER or BIGINT, respectively with a default set to nextval('table_name_column_name_seq'::regclass)
    - Using SERIAL or BIGSERIAL automatically makes the column NOT NULL.
2. Aliases:
    - There are many aliases such as VARCHAR for CHARACTER VARYING, TIMESTAMPTZ for TIMESTAMP WITH TIME ZONE, etc.
    - Postgres internally stores expanded versions, so PostgresInspector should return the expanded version of the type.
3. CHECK constraints:
    - CHECK constraints are internally stored as strings for every column referenced in the CHECK constraint.
    - Thus, PostgresInspector returns CHECK constaint for every column that is referenced in the CHECK constraint.
"""

import pytest
from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig
from skibidi_orm.migration_engine.db_inspectors.postgres_inspector import (
    PostgresInspector,
)
from ..conftest import postgres_db_fixture
from ..sql_data import PostgresTablesData, SQLite3TablesData
import skibidi_orm.migration_engine.adapters.database_objects.constraints as c


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


@pytest.mark.parametrize(
    "query, table_name, column_name, expected_nullable",
    [
        (  # 0
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "text_not_null",
            False,
        ),
        (  # 1
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "text_nullabe",
            True,
        ),
        (  # 2
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "integer_not_null",
            False,
        ),
        (  # 3
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "integer_nullable",
            True,
        ),
        (  # 4
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "date_not_null",
            False,
        ),
        (  # 5
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "date_nullable",
            True,
        ),
        (  # 6
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            "primary_key",
            False,
        ),
    ],
)
def test__is_column_nullable(query, table_name, column_name, expected_nullable):  # type: ignore
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
        assert inspector._is_column_nullable(table_name, column_name) is expected_nullable  # type: ignore

    test_fn()


@pytest.mark.parametrize(
    "query, table_name, column_name, expected_constraints",
    [
        (  # 0
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "primary_key",
            [
                c.NotNullConstraint("table_different_constraints", "primary_key"),
                c.PrimaryKeyConstraint("table_different_constraints", "primary_key"),
            ],
        ),
        (  # 1
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "text_nullable",
            [],
        ),
        (  # 2
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "integer_not_nullable",
            [
                c.NotNullConstraint(
                    "table_different_constraints", "integer_not_nullable"
                ),
                c.CheckConstraint(
                    "table_different_constraints",
                    "integer_not_nullable",
                    "((integer_not_nullable > 100))",
                ),
            ],
        ),
        (  # 3
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "unique_column",
            [c.UniqueConstraint("table_different_constraints", "unique_column")],
        ),
        (  # 4
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "unique_not_nullable",
            [
                c.UniqueConstraint(
                    "table_different_constraints", "unique_not_nullable"
                ),
                c.NotNullConstraint(
                    "table_different_constraints", "unique_not_nullable"
                ),
            ],
        ),
        (  # 5
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "check_other_column",
            [],
        ),
        (  # 6
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "default_column",
            [c.DefaultConstraint("table_different_constraints", "default_column", "1")],
        ),
        (  # 7
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "not_null_unique_check_column",
            [
                c.NotNullConstraint(
                    "table_different_constraints", "not_null_unique_check_column"
                ),
                c.UniqueConstraint(
                    "table_different_constraints", "not_null_unique_check_column"
                ),
                c.CheckConstraint(
                    "table_different_constraints",
                    "not_null_unique_check_column",
                    "((not_null_unique_check_column > 100))",
                ),
            ],
        ),
        (  # 8
            PostgresTablesData.SQL_TABLE_SIMPLE_FOREIGN_KEYS,
            "authors",
            "id",
            [
                c.NotNullConstraint("authors", "id"),
                c.PrimaryKeyConstraint("authors", "id"),
                c.DefaultConstraint(
                    "authors", "id", "nextval('authors_id_seq'::regclass)"
                ),
            ],
        ),
        (  # 9
            PostgresTablesData.SQL_TABLE_SIMPLE_FOREIGN_KEYS,
            "books",
            "author_id_foreign_key",
            [],
        ),
        (  # 10
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "not_null_unique",
            [
                c.NotNullConstraint("table_different_constraints", "not_null_unique"),
                c.UniqueConstraint("table_different_constraints", "not_null_unique"),
            ],
        ),
        (  # 11
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "not_null_default",
            [
                c.NotNullConstraint("table_different_constraints", "not_null_default"),
                c.DefaultConstraint(
                    "table_different_constraints", "not_null_default", "1"
                ),
            ],
        ),
        (  # 12
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            "not_null_unique_check_default",
            [
                c.NotNullConstraint(
                    "table_different_constraints", "not_null_unique_check_default"
                ),
                c.UniqueConstraint(
                    "table_different_constraints", "not_null_unique_check_default"
                ),
                c.DefaultConstraint(
                    "table_different_constraints", "not_null_unique_check_default", "1"
                ),
                c.CheckConstraint(
                    "table_different_constraints",
                    "not_null_unique_check_default",
                    "((not_null_unique_check_default > 100))",
                ),
            ],
        ),
        (  # 13
            [PostgresTablesData.SQL_TABLE_SERIALS],
            "table_serials",
            "serial_pk",
            [
                c.DefaultConstraint(
                    "table_serials",
                    "serial_pk",
                    "nextval('table_serials_serial_pk_seq'::regclass)",
                ),
                c.NotNullConstraint("table_serials", "serial_pk"),
                c.PrimaryKeyConstraint("table_serials", "serial_pk"),
            ],
        ),
        (  # 14
            [PostgresTablesData.SQL_TABLE_SERIALS],
            "table_serials",
            "bigserial",
            [
                c.DefaultConstraint(
                    "table_serials",
                    "bigserial",
                    "nextval('table_serials_bigserial_seq'::regclass)",
                ),
                c.NotNullConstraint("table_serials", "bigserial"),
            ],
        ),
    ],
)
def test__get_column_constraints(query, table_name, column_name, expected_constraints):  # type: ignore
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
        constraints = inspector._get_column_constraints(table_name, column_name)  # type: ignore
        assert sorted(constraints) == sorted(expected_constraints)  # type: ignore

    test_fn()
