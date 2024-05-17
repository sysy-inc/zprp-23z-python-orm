import pytest

from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    NotNullConstraint,
    PrimaryKeyConstraint,
)
from skibidi_orm.migration_engine.adapters.database_objects.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.data_mutator.base_data_mutator import InsertRowColumn
from skibidi_orm.migration_engine.data_mutator.sqlite3_data_mutatorr import (
    SQLite3DataMutator,
)
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import SqliteInspector

sql_simple_db = [
    """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL
    );
"""
]


@pytest.mark.parametrize("make_database", [[*sql_simple_db]], indirect=True)
def test_insert_row(make_database: str):
    SQLite3Config(db_path=make_database)
    db_seeder = SQLite3DataMutator()
    db_seeder.insert_row(
        table_name="users",
        row=[
            InsertRowColumn(name="user_id", value=str(1)),
            InsertRowColumn(name="username", value="test"),
        ],
    )
    db_inspector = SqliteInspector()
    tables = db_inspector.get_tables()

    assert tables[0] == SQLite3Typing.Table(
        name="users",
        columns=[
            SQLite3Typing.Column(
                name="user_id",
                data_type="INTEGER",
                constraints=[
                    PrimaryKeyConstraint(table_name="users", column_name="user_id"),
                ],
            ),
            SQLite3Typing.Column(
                name="username",
                data_type="TEXT",
                constraints=[
                    NotNullConstraint(table_name="users", column_name="username"),
                ],
            ),
        ],
    )
