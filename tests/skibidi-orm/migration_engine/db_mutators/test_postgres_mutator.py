import pytest

from skibidi_orm.migration_engine.data_mutator.postgres_data_mutator import (
    PostgresDataMutator,
)
from ..conftest import postgres_db_fixture
from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig
from skibidi_orm.migration_engine.db_inspectors.postgres_inspector import (
    PostgresInspector,
)


@pytest.mark.parametrize(
    "create_query, query, expected",
    [
        (
            [
                "CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT);",
                "INSERT INTO test (name) VALUES ('test');",
            ],
            "SELECT * FROM test;",
            [
                (1, "test"),
            ],
        ),
        (
            ["CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT);"],
            "INSERT INTO test (name) VALUES ('test');",
            [],
        ),
        (
            ["CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT);"],
            "SELECT * FROM test;",
            [],
        ),
    ],
)
def test_raw_query(create_query, query, expected):  # type: ignore
    @postgres_db_fixture(
        db_name="postgres",
        db_user="admin",
        db_password="admin",
        db_host="0.0.0.0",
        db_port=5432,
        queries=create_query,  # type: ignore
    )
    def test_fn(config: PostgresConfig, inspector: PostgresInspector):
        mutator = PostgresDataMutator()
        result = mutator.raw_query(query)  # type: ignore
        assert result == expected

    test_fn()


@pytest.mark.parametrize(
    "create_query, table_name, limit, offset, expected",
    [
        (
            ["CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT);"],
            "test",
            100,
            0,
            [],
        ),
        (
            [
                "CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT);",
                "INSERT INTO test (name) VALUES ('test');",
            ],
            "test",
            100,
            0,
            [(1, "test")],
        ),
        (
            [
                "CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT);",
                "INSERT INTO test (name) VALUES ('test');",
            ],
            "test",
            1,
            1,
            [],
        ),
        (
            [
                "CREATE TABLE test (id SERIAL PRIMARY KEY, name TEXT);",
                "INSERT INTO test (name) VALUES ('test');",
            ],
            "test",
            0,
            0,
            [],
        ),
    ],
)
def test_get_rows(create_query, table_name, limit, offset, expected):  # type: ignore
    @postgres_db_fixture(
        db_name="postgres",
        db_user="admin",
        db_password="admin",
        db_host="0.0.0.0",
        db_port=5432,
        queries=create_query,  # type: ignore
    )
    def test_fn(config: PostgresConfig, inspector: PostgresInspector):
        mutator = PostgresDataMutator()
        results = mutator.get_rows(table_name=table_name, limit=limit, offset=offset)  # type: ignore
        assert sorted(results) == sorted(expected)  # type: ignore

    test_fn()
