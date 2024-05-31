from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    ForeignKeyConstraint,
)
from skibidi_orm.migration_engine.adapters.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.adapters.providers import DatabaseProvider
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import (
    SQLite3Inspector,
)
from skibidi_orm.migration_engine.revisions.manager import RevisionManager
from skibidi_orm.migration_engine.revisions.revision import Revision
import pytest

sql_schema_with_fks = [
    # todo: remove after postgres is merged
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

simple_testing_schema = [
    "CREATE TABLE test_table (id INTEGER, name TEXT);",
    "CREATE TABLE test_table_2 (idd INTEGER, count_ INTEGER, FOREIGN KEY (idd) REFERENCES test_table (id));",
    "INSERT INTO test_table (id, name) VALUES (1, 'test');",
]

table_1 = SQLite3Typing.Table(
    "test_table",
    [SQLite3Typing.Column("id", "INTEGER"), SQLite3Typing.Column("name", "TEXT")],
)

table_2 = SQLite3Typing.Table(
    "test_table_2",
    [
        SQLite3Typing.Column("idd", "INTEGER"),
        SQLite3Typing.Column("count_", "INTEGER"),
    ],
    {ForeignKeyConstraint("test_table_2", "test_table", {"idd": "id"})},
)

revision_1 = Revision(
    "test description",
    "test schema repr",
    DatabaseProvider.SQLITE3,
    [table_1, table_2],
)

revision_2 = Revision(
    "test description_2",
    "test schema repr_2",
    DatabaseProvider.SQLITE3,
    [SQLite3Typing.Table("test_table", [])],
)


def test_create_and_find_revision_table_sqlite(
    make_database: str, monkeypatch: pytest.MonkeyPatch
):
    """Tests whether the revision table is found if it does not exist"""
    monkeypatch.setattr(RevisionManager, "create_revision_table", lambda _: None)  # type: ignore
    monkeypatch.setattr(RevisionManager, "get_all_revisions", lambda _: [])  # type: ignore

    SQLite3Config(make_database)
    manager = RevisionManager()
    assert not manager.find_revision_table()


def test_save_revision_sqlite(make_database: str):
    """Tests whether a revision can be saved without causing
    any database errors"""
    SQLite3Config(make_database)
    manager = RevisionManager()

    if not manager.find_revision_table():
        manager.create_revision_table()
    manager.save_revision(revision_1)


def test_save_and_get_revision_sqlite(make_database: str):
    """Tests whether a revision can be saved and then retrieved
    from the database"""
    SQLite3Config(make_database)
    manager = RevisionManager()

    if not manager.find_revision_table():
        manager.create_revision_table()

    manager.save_revision(revision_1)
    manager.save_revision(revision_2)

    revisions = manager.get_all_revisions()

    assert len(revisions) == 2
    assert revisions[1] == revision_1
    assert revisions[2] == revision_2


@pytest.mark.parametrize("make_database", [simple_testing_schema], indirect=True)
def test_clear_database_sqlite(make_database: str):
    """Clearing the database removes everything but the revisions table and its contents"""
    SQLite3Config(make_database)
    manager = RevisionManager()

    manager.save_revision(revision_1)
    manager.clear_database()

    revisions = manager.get_all_revisions()
    assert len(revisions) == 1
    revision_ = revisions.values().__iter__().__next__()
    assert revision_ == revision_1


@pytest.mark.parametrize("make_database", [simple_testing_schema], indirect=True)
def test_get_revision_SQL_sqlite(make_database: str):
    SQLite3Config(make_database)
    manager = RevisionManager()

    revision_sql = manager.get_revision_SQL(revision_1)
    assert revision_sql == (
        "CREATE TABLE test_table (id INTEGER, name TEXT);\n"
        "CREATE TABLE test_table_2 (idd INTEGER, count_ INTEGER, FOREIGN KEY (idd) "
        "REFERENCES test_table (id));"
    )


def test_go_to_revision_from_empty_db_sqlite(make_database: str):
    """Tests whether the go_to_revision method works when the database is empty"""
    SQLite3Config(make_database)

    manager = RevisionManager()
    manager.save_revision(revision_1)
    revision_id = manager.get_all_revisions().keys().__iter__().__next__()

    assert manager.get_revision_by_id(revision_id) == revision_1
    manager.go_to_revision(revision_1)

    all_tables = SQLite3Inspector().get_tables()

    assert len(all_tables) == 2
    assert table_1 in all_tables
    assert table_2 in all_tables


@pytest.mark.parametrize("make_database", [sql_schema_with_fks], indirect=True)
def test_go_to_revision_from_non_empty_db_sqlite(make_database: str):
    SQLite3Config(make_database)
    inspector = SQLite3Inspector()
    assert len(inspector.get_tables()) == 3

    manager = RevisionManager()
    manager.go_to_revision(revision_1)
    new_tables = inspector.get_tables()
    assert table_1 in new_tables
    assert table_2 in new_tables
    assert len(new_tables) == 2
