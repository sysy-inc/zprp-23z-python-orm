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
4. DEFAULT constraints:
    - Some default constaints are stored as is, e.g.
        `my_col INTEGER DEFAULT 1`, will store `1` as the default value.
    - Other default constaints are stored with type casting, e.g.
        `my_col TEXT DEFAULT 'default'`, will store `'default'::text` as the default value.
    - Other default constaints store functions names, e.g.
        `my_col DATE DEFAULT CURRENT_DATE`, will store `CURRENT_DATE` as the default value.
    - PostgresInspector returns the default values as stored internally by Postgres.
"""

import pytest
from skibidi_orm.migration_engine.adapters.postgres_typing import PostgresTyping
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
        (  # 15
            [PostgresTablesData.SQL_TABLE_DEFAULTS],
            "table_defaults",
            "integer_default",
            [
                c.DefaultConstraint(
                    "table_defaults",
                    "integer_default",
                    "1",
                ),
            ],
        ),
        (  # 16
            [PostgresTablesData.SQL_TABLE_DEFAULTS],
            "table_defaults",
            "text_default",
            [
                c.DefaultConstraint(
                    "table_defaults",
                    "text_default",
                    "'default'::text",
                ),
            ],
        ),
        (  # 17
            [PostgresTablesData.SQL_TABLE_DEFAULTS],
            "table_defaults",
            "date_default",
            [
                c.DefaultConstraint(
                    "table_defaults",
                    "date_default",
                    "CURRENT_DATE",
                ),
            ],
        ),
        (  # 18
            [PostgresTablesData.SQL_TABLE_DEFAULTS],
            "table_defaults",
            "timestamp_default",
            [
                c.DefaultConstraint(
                    "table_defaults",
                    "timestamp_default",
                    "CURRENT_TIMESTAMP",
                ),
            ],
        ),
        (  # 19
            [PostgresTablesData.SQL_TABLE_DEFAULTS],
            "table_defaults",
            "timestamp_default_lowercase",
            [
                c.DefaultConstraint(
                    "table_defaults",
                    "timestamp_default_lowercase",
                    "CURRENT_TIMESTAMP",
                ),
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


@pytest.mark.parametrize(
    "query, table_name, expected_columns",
    [
        (  # 0
            [PostgresTablesData.SQL_TABLE_MANY_COLUMNS1],
            "table_many_columns1",
            [
                PostgresTyping.Column(
                    name="primary_key",
                    data_type="INTEGER",
                    column_constraints=[
                        c.NotNullConstraint("table_many_columns1", "primary_key"),
                        c.PrimaryKeyConstraint("table_many_columns1", "primary_key"),
                    ],
                ),
                PostgresTyping.Column(
                    name="text_not_null",
                    data_type="TEXT",
                    column_constraints=[
                        c.NotNullConstraint("table_many_columns1", "text_not_null"),
                    ],
                ),
                PostgresTyping.Column(
                    name="text_nullabe",
                    data_type="TEXT",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="integer_not_null",
                    data_type="INTEGER",
                    column_constraints=[
                        c.NotNullConstraint("table_many_columns1", "integer_not_null"),
                    ],
                ),
                PostgresTyping.Column(
                    name="integer_nullable",
                    data_type="INTEGER",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="date_not_null",
                    data_type="DATE",
                    column_constraints=[
                        c.NotNullConstraint("table_many_columns1", "date_not_null"),
                    ],
                ),
                PostgresTyping.Column(
                    name="date_nullable",
                    data_type="DATE",
                    column_constraints=[],
                ),
            ],
        ),
        (  # 1
            [PostgresTablesData.SQL_TABLE_DIFFICULT_TYPES],
            "table_difficult_types",
            [
                PostgresTyping.Column(
                    name="big_primary_key_alias",
                    data_type="BIGINT",
                    column_constraints=[
                        c.DefaultConstraint(
                            "table_difficult_types",
                            "big_primary_key_alias",
                            "nextval('table_difficult_types_big_primary_key_alias_seq'::regclass)",
                        ),
                        c.NotNullConstraint(
                            "table_difficult_types", "big_primary_key_alias"
                        ),
                        c.PrimaryKeyConstraint(
                            "table_difficult_types",
                            "big_primary_key_alias",
                        ),
                    ],
                ),
                PostgresTyping.Column(
                    name="bit_varying_alias",
                    data_type="BIT VARYING",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="bit_varying_alias_arg",
                    data_type="BIT VARYING",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="double_precision",
                    data_type="DOUBLE PRECISION",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="timestamp",
                    data_type="TIMESTAMP WITHOUT TIME ZONE",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="timestamp_arg",
                    data_type="TIMESTAMP WITHOUT TIME ZONE",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="timestamp_without_time_zone",
                    data_type="TIMESTAMP WITHOUT TIME ZONE",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="timestamp_without_time_zone_arg",
                    data_type="TIMESTAMP WITHOUT TIME ZONE",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="timestamp_with_time_zone_alias",
                    data_type="TIMESTAMP WITH TIME ZONE",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="timestamp_with_time_zone_arg_alias",
                    data_type="TIMESTAMP WITH TIME ZONE",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="charachter_varying",
                    data_type="CHARACTER VARYING",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="charachter_varying_arg",
                    data_type="CHARACTER VARYING",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="charachter_varying_alias",
                    data_type="CHARACTER VARYING",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="charachter_varying_alias_args",
                    data_type="CHARACTER VARYING",
                    column_constraints=[],
                ),
            ],
        ),
        (  # 2
            [PostgresTablesData.SQL_TABLE_DIFFERECT_CONSTRAINTS],
            "table_different_constraints",
            [
                PostgresTyping.Column(
                    name="primary_key",
                    data_type="INTEGER",
                    column_constraints=[
                        c.NotNullConstraint(
                            "table_different_constraints", "primary_key"
                        ),
                        c.PrimaryKeyConstraint(
                            "table_different_constraints", "primary_key"
                        ),
                    ],
                ),
                PostgresTyping.Column(
                    name="integer_not_nullable",
                    data_type="INTEGER",
                    column_constraints=[
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
                PostgresTyping.Column(
                    name="text_nullable",
                    data_type="TEXT",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="unique_column",
                    data_type="INTEGER",
                    column_constraints=[
                        c.UniqueConstraint(
                            "table_different_constraints", "unique_column"
                        ),
                    ],
                ),
                PostgresTyping.Column(
                    name="unique_not_nullable",
                    data_type="INTEGER",
                    column_constraints=[
                        c.UniqueConstraint(
                            "table_different_constraints", "unique_not_nullable"
                        ),
                        c.NotNullConstraint(
                            "table_different_constraints", "unique_not_nullable"
                        ),
                    ],
                ),
                PostgresTyping.Column(
                    name="check_other_column",
                    data_type="INTEGER",
                    column_constraints=[],
                ),
                PostgresTyping.Column(
                    name="default_column",
                    data_type="INTEGER",
                    column_constraints=[
                        c.DefaultConstraint(
                            "table_different_constraints", "default_column", "1"
                        ),
                    ],
                ),
                PostgresTyping.Column(
                    name="not_null_unique_check_column",
                    data_type="INTEGER",
                    column_constraints=[
                        c.NotNullConstraint(
                            "table_different_constraints",
                            "not_null_unique_check_column",
                        ),
                        c.UniqueConstraint(
                            "table_different_constraints",
                            "not_null_unique_check_column",
                        ),
                        c.CheckConstraint(
                            "table_different_constraints",
                            "not_null_unique_check_column",
                            "((not_null_unique_check_column > 100))",
                        ),
                    ],
                ),
                PostgresTyping.Column(
                    name="not_null_unique",
                    data_type="INTEGER",
                    column_constraints=[
                        c.NotNullConstraint(
                            "table_different_constraints", "not_null_unique"
                        ),
                        c.UniqueConstraint(
                            "table_different_constraints", "not_null_unique"
                        ),
                    ],
                ),
                PostgresTyping.Column(
                    name="not_null_default",
                    data_type="INTEGER",
                    column_constraints=[
                        c.NotNullConstraint(
                            "table_different_constraints", "not_null_default"
                        ),
                        c.DefaultConstraint(
                            "table_different_constraints", "not_null_default", "1"
                        ),
                    ],
                ),
                PostgresTyping.Column(
                    name="not_null_unique_check_default",
                    data_type="INTEGER",
                    column_constraints=[
                        c.NotNullConstraint(
                            "table_different_constraints",
                            "not_null_unique_check_default",
                        ),
                        c.UniqueConstraint(
                            "table_different_constraints",
                            "not_null_unique_check_default",
                        ),
                        c.DefaultConstraint(
                            "table_different_constraints",
                            "not_null_unique_check_default",
                            "1",
                        ),
                        c.CheckConstraint(
                            "table_different_constraints",
                            "not_null_unique_check_default",
                            "((not_null_unique_check_default > 100))",
                        ),
                    ],
                ),
            ],
        ),
    ],
)
def test_get_table_columns(query, table_name, expected_columns):  # type: ignore
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
        columns = inspector.get_table_columns(table_name)  # type: ignore
        for column in columns:
            column.column_constraints = sorted(column.column_constraints)
        for column in expected_columns:  # type: ignore
            column.column_constraints = sorted(column.column_constraints)  # type: ignore
        assert sorted(columns) == sorted(expected_columns)  # type: ignore

    test_fn()


@pytest.mark.parametrize(
    "query, table_name, expected_foreign_keys",
    [
        (  # 0
            PostgresTablesData.SQL_TABLE_FKS_MORE_COMPLEX,
            "departments",
            set(),  # type: ignore
        ),
        (  # 1
            PostgresTablesData.SQL_TABLE_FKS_MORE_COMPLEX,
            "employees",
            set(
                [
                    c.ForeignKeyConstraint(
                        table_name="employees",
                        referenced_table="departments",
                        column_mapping={
                            "department_id": "department_id",
                        },
                    )
                ]
            ),
        ),
        (  # 2
            PostgresTablesData.SQL_TABLE_FKS_MORE_COMPLEX,
            "projects",
            set(
                [
                    c.ForeignKeyConstraint(
                        table_name="projects",
                        referenced_table="employees",
                        column_mapping={
                            "lead_employee_id": "employee_id",
                        },
                    ),
                    c.ForeignKeyConstraint(
                        table_name="projects",
                        referenced_table="departments",
                        column_mapping={
                            "support_department_id": "department_id",
                        },
                    ),
                ]
            ),
        ),
    ],
)
def test__get_foreign_keys(query, table_name, expected_foreign_keys):  # type: ignore
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
        foreign_keys = inspector._get_foreign_keys(table_name)  # type: ignore
        print("=============================")
        print(foreign_keys)
        print("=============================")
        assert foreign_keys == expected_foreign_keys

    test_fn()
