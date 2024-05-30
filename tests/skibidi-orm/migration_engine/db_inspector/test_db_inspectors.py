from pathlib import Path
import pytest

from skibidi_orm.migration_engine.adapters.database_objects.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.adapters.database_objects import constraints as c
import sqlite3

from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import (
    SQLite3Inspector,
)
from skibidi_orm.migration_engine.revisions.manager import RevisionManager

sql_table1 = """
    CREATE TABLE table1 (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
"""
sql_table2 = """
    CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
"""
sql_table_primary_key_not_null = """
    CREATE TABLE table_primary_key_not_null (
        id INTEGER PRIMARY KEY NOT NULL
    );
"""

sql_schema_with_fks = [
    """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""",
    """
    CREATE TABLE posts (
        post_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
""",
    """
    CREATE TABLE comments (
        comment_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        user_idd INTEGER NOT NULL,
        post_id INTEGER NOT NULL,
        comment_text TEXT NOT NULL,
        comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_idd, username) REFERENCES users(user_id, username),
        FOREIGN KEY (post_id) REFERENCES posts(post_id)
    );
""",
]

sql_simple_schema_with_fks = [
    # a simpler schema, without constraints that are not supported yet, only containing fks, primary key and not null
    """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password_hash TEXT NOT NULL,
        registration_date TIMESTAMP NOT NULL
        );
    """,
    """
    CREATE TABLE posts (
        post_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        post_date TIMESTAMP NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
    """,
    """CREATE TABLE comments (
        comment_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        user_idd INTEGER NOT NULL,
        post_id INTEGER NOT NULL,
        comment_text TEXT NOT NULL,
        comment_date TIMESTAMP NOT NULL,
        FOREIGN KEY (user_idd, username) REFERENCES users(user_id, username),
        FOREIGN KEY (post_id) REFERENCES posts(post_id)
    );
    """,
]


def execute_sqlite3_commands(db_path: str, commands: list[str]):
    """Executes the given commands in a SQLite DB living under db_path"""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        conn.commit()
        cursor.close()


@pytest.fixture
def tmp_database(request: pytest.FixtureRequest, tmp_path: Path):
    """Fixture for creating a temporary database and executing sqlite3 code. Yields the
    path of the db file."""
    sql_commands = request.param
    (tmp_file := tmp_path.joinpath("tmp_db.db")).touch()
    execute_sqlite3_commands(
        str(tmp_file),
        sql_commands,
    )
    yield str(tmp_file)


@pytest.mark.parametrize("tmp_database", [[sql_table1, sql_table2]], indirect=True)
@pytest.mark.usefixtures("tmp_database")
def test_can_only_be_instantiated_with_sqlite3config_instantiated_earlier():
    with pytest.raises(ReferenceError) as exc_info:
        SQLite3Inspector()
    assert str(exc_info.value) == "Instance does not exist"


@pytest.mark.parametrize("tmp_database", [[sql_table1, sql_table2]], indirect=True)
def test_get_tables_names(tmp_database: str):
    SQLite3Config(tmp_database)
    inspector = SQLite3Inspector()
    tables = inspector.get_tables_names()
    assert len(tables) == 2
    assert tables[0] == "table1"
    assert tables[1] == "table2"


@pytest.mark.parametrize("tmp_database", [[sql_table1, sql_table2]], indirect=True)
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
    "tmp_database", [[sql_table_primary_key_not_null]], indirect=True
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


@pytest.mark.parametrize("tmp_database", [[sql_table1, sql_table2]], indirect=True)
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


@pytest.mark.parametrize("tmp_database", [sql_schema_with_fks], indirect=True)
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


@pytest.mark.parametrize("tmp_database", [sql_simple_schema_with_fks], indirect=True)
def test_get_tables_fk_schema(tmp_database: str):
    SQLite3Config(db_path=tmp_database)
    inspector = SQLite3Inspector()
    tables = inspector.get_tables()
    table_1 = SQLite3Typing.Table(
        "users",
        [
            SQLite3Typing.Column(
                "user_id", "INTEGER", [c.PrimaryKeyConstraint("users", "user_id")]
            ),
            SQLite3Typing.Column(
                "username",
                "TEXT",
                [
                    c.NotNullConstraint("users", "username"),
                ],
            ),
            SQLite3Typing.Column(
                "email",
                "TEXT",
                [
                    c.NotNullConstraint("users", "email"),
                ],
            ),
            SQLite3Typing.Column(
                "password_hash", "TEXT", [c.NotNullConstraint("users", "password_hash")]
            ),
            SQLite3Typing.Column(
                "registration_date",
                "TIMESTAMP",
                [c.NotNullConstraint("users", "registration_date")],
            ),
        ],
    )
    table_2 = SQLite3Typing.Table(
        "posts",
        [
            SQLite3Typing.Column(
                "post_id", "INTEGER", [c.PrimaryKeyConstraint("posts", "post_id")]
            ),
            SQLite3Typing.Column(
                "user_id", "INTEGER", [c.NotNullConstraint("posts", "user_id")]
            ),
            SQLite3Typing.Column(
                "title", "TEXT", [c.NotNullConstraint("posts", "title")]
            ),
            SQLite3Typing.Column(
                "content", "TEXT", [c.NotNullConstraint("posts", "content")]
            ),
            SQLite3Typing.Column(
                "post_date", "TIMESTAMP", [c.NotNullConstraint("posts", "post_date")]
            ),
        ],
        {c.ForeignKeyConstraint("posts", "users", {"user_id": "user_id"})},
    )

    table_3 = SQLite3Typing.Table(
        "comments",
        [
            SQLite3Typing.Column(
                "comment_id",
                "INTEGER",
                [c.PrimaryKeyConstraint("comments", "comment_id")],
            ),
            SQLite3Typing.Column(
                "username", "TEXT", [c.NotNullConstraint("comments", "username")]
            ),
            SQLite3Typing.Column(
                "user_idd", "INTEGER", [c.NotNullConstraint("comments", "user_idd")]
            ),
            SQLite3Typing.Column(
                "post_id", "INTEGER", [c.NotNullConstraint("comments", "post_id")]
            ),
            SQLite3Typing.Column(
                "comment_text",
                "TEXT",
                [c.NotNullConstraint("comments", "comment_text")],
            ),
            SQLite3Typing.Column(
                "comment_date",
                "TIMESTAMP",
                [c.NotNullConstraint("comments", "comment_date")],
            ),
        ],
        {
            c.ForeignKeyConstraint(
                "comments", "users", {"user_idd": "user_id", "username": "username"}
            ),
            c.ForeignKeyConstraint("comments", "posts", {"post_id": "post_id"}),
        },
    )

    assert len(tables) == 3
    assert table_1 in tables
    assert table_2 in tables
    assert table_3 in tables


def test_revision_table_hidden_from_inspector_sqlite(make_database: str):
    """Tests whether the revision table is hidden from the sqlite inspector"""
    SQLite3Config(db_path=make_database)
    inspector = SQLite3Inspector()
    RevisionManager()  # creates the revision table in init
    tables = inspector.get_tables_names()
    assert len(tables) == 0
