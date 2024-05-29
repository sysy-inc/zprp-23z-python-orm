import pathlib
import pytest
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.adapters.database_objects import constraints as c
import sqlite3

from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import (
    SQLite3Inspector,
)

from ..sql_data import SQLite3TablesData


def execute_sqlite3_commands(db_path: str, commands: list[str]):
    """Executes the given commands in a SQLite DB living under db_path"""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        conn.commit()
        cursor.close()


@pytest.fixture
def tmp_database(request: pytest.FixtureRequest, tmp_path: pathlib.Path):
    """Fixture for creating a temporary database and executing sqlite3 code. Yields the
    path of the db file."""
    sql_commands = request.param
    (tmp_file := tmp_path.joinpath("tmp_db.db")).touch()
    execute_sqlite3_commands(
        str(tmp_file),
        sql_commands,
    )
    yield str(tmp_file)


@pytest.mark.parametrize(
    "tmp_database",
    [[SQLite3TablesData.sql_table1, SQLite3TablesData.sql_table2]],
    indirect=True,
)
@pytest.mark.usefixtures("tmp_database")
def test_can_only_be_instantiated_with_sqlite3config_instantiated_earlier():
    with pytest.raises(ReferenceError) as exc_info:
        SQLite3Inspector()
    assert str(exc_info.value) == "Instance does not exist"


@pytest.mark.parametrize(
    "tmp_database",
    [[SQLite3TablesData.sql_table1, SQLite3TablesData.sql_table2]],
    indirect=True,
)
def test_get_tables_names(tmp_database: str):
    SQLite3Config(tmp_database)
    inspector = SQLite3Inspector()
    tables = inspector.get_tables_names()
    assert len(tables) == 2
    assert tables[0] == "table1"
    assert tables[1] == "table2"


@pytest.mark.parametrize(
    "tmp_database",
    [[SQLite3TablesData.sql_table1, SQLite3TablesData.sql_table2]],
    indirect=True,
)
def test_get_table_columns(tmp_database: str):
    SQLite3Config(db_path=tmp_database)
    inspector = SQLite3Inspector()
    columns = inspector.get_table_columns("table1")
    assert columns[0].name == "id"
    assert columns[0].data_type == "INTEGER"
    assert columns[0].column_constraints == [c.PrimaryKeyConstraint("table1", "id")]
    assert columns[1].name == "name"
    assert columns[1].data_type == "TEXT"
    assert columns[1].column_constraints == [c.NotNullConstraint("table1", "name")]
    assert len(columns) == 2


@pytest.mark.parametrize(
    "tmp_database", [[SQLite3TablesData.sql_table_primary_key_not_null]], indirect=True
)
def test_get_table_columns__primaryk_notnull(tmp_database: str):
    SQLite3Config(db_path=tmp_database)
    inspector = SQLite3Inspector()
    columns = inspector.get_table_columns("table_primary_key_not_null")
    assert columns[0].name == "id"
    assert columns[0].data_type == "INTEGER"
    assert columns[0].column_constraints == [
        c.PrimaryKeyConstraint("table_primary_key_not_null", "id"),
        c.NotNullConstraint("table_primary_key_not_null", "id"),
    ]


@pytest.mark.parametrize(
    "tmp_database",
    [[SQLite3TablesData.sql_table1, SQLite3TablesData.sql_table2]],
    indirect=True,
)
def test_get_tables(tmp_database: str):
    SQLite3Config(db_path=tmp_database)
    inspector = SQLite3Inspector()
    tables = inspector.get_tables()
    assert len(tables) == 2
    assert tables[0].name == "table1"
    assert tables[1].name == "table2"
    assert len(tables[0].columns) == 2
    assert len(tables[1].columns) == 2
    assert tables[0].columns[0].name == "id"
    assert tables[0].columns[0].data_type == "INTEGER"
    assert tables[0].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("table1", "id")
    ]
    assert tables[0].columns[1].name == "name"
    assert tables[0].columns[1].data_type == "TEXT"
    assert tables[0].columns[1].column_constraints == [
        c.NotNullConstraint("table1", "name")
    ]
    assert tables[1].columns[0].name == "id"
    assert tables[1].columns[0].data_type == "INTEGER"
    assert tables[1].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("table2", "id")
    ]
    assert tables[1].columns[1].name == "name"
    assert tables[1].columns[1].data_type == "TEXT"
    assert tables[1].columns[1].column_constraints == [
        c.NotNullConstraint("table2", "name")
    ]


@pytest.mark.parametrize(
    "tmp_database", [[*SQLite3TablesData.sql_schema_with_fks]], indirect=True
)
def test_get_foreign_keys(tmp_database: str):
    SQLite3Config(db_path=tmp_database)
    inspector = SQLite3Inspector()
    foreign_keys = inspector.get_foreign_key_constraints()
    assert len(foreign_keys) == 3
    correct_fk_set = {
        c.ForeignKeyConstraint("posts", "users", {"user_id": "user_id"}),
        c.ForeignKeyConstraint(
            "comments", "users", {"user_idd": "user_id", "username": "username"}
        ),
        c.ForeignKeyConstraint("comments", "posts", {"post_id": "post_id"}),
    }
    assert correct_fk_set.intersection(foreign_keys) == foreign_keys
