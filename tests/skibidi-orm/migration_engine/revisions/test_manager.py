from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    ForeignKeyConstraint,
)
from skibidi_orm.migration_engine.adapters.database_objects.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.adapters.providers import DatabaseProvider
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import (
    SQLite3Inspector,
)
from skibidi_orm.migration_engine.revisions.manager import RevisionManager
from skibidi_orm.migration_engine.revisions.revision import Revision
from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor


# TODO: test this somehow even though it's done in init
# def test_create_and_find_revision_table_sqlite(make_database: str):
#     """Tests whether the revision table is found if it does not exist"""
#     SQLite3Config(make_database)
#     manager = RevisionManager()
#     assert not manager.find_revision_table()
#     manager.create_revision_table()
#     assert manager.find_revision_table()
#


def test_save_revision_sqlite(make_database: str):
    """Tests whether a revision can be saved without causing
    any database errors"""
    SQLite3Config(make_database)
    manager = RevisionManager()
    if not manager.find_revision_table():
        manager.create_revision_table()
    revision = Revision(
        "test description",
        "test schema repr",
        DatabaseProvider.SQLITE3,
        [],
    )
    manager.save_revision(revision)


def test_save_and_get_revision_sqlite(make_database: str):
    """Tests whether a revision can be saved and then retrieved
    from the database"""
    SQLite3Config(make_database)
    manager = RevisionManager()
    if not manager.find_revision_table():
        manager.create_revision_table()
    revision = Revision(
        "test description",
        "test schema repr",
        DatabaseProvider.SQLITE3,
        [],
    )
    revision_2 = Revision(
        "test description_2",
        "test schema repr_2",
        DatabaseProvider.SQLITE3,
        [SQLite3Typing.Table("test_table", [])],
    )
    manager.save_revision(revision)
    manager.save_revision(revision_2)
    revisions = manager.get_all_revisions()
    assert len(revisions) == 2
    assert revisions[1] == revision
    assert revisions[2] == revision_2


def test_clear_database_sqlite(make_database: str):
    """Clearing the database removes everything but the revisions table and its contents"""
    SQLite3Config(make_database)
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
    SQLite3Executor.execute_sql(
        """
        CREATE TABLE test_table (id INTEGER, name TEXT);
        CREATE TABLE test_table_2 (idd INTEGER, count_ INTEGER, FOREIGN KEY (idd) REFERENCES test_table (id));
        INSERT INTO test_table (id, name) VALUES (1, 'test');
        """
    )
    manager = RevisionManager()
    revision = Revision(
        "test description",
        "test schema repr",
        DatabaseProvider.SQLITE3,
        [table_1, table_2],
    )
    manager.save_revision(revision)
    manager.clear_database()
    revisions = manager.get_all_revisions()
    assert len(revisions) == 1
    revision_ = revisions.values().__iter__().__next__()
    assert revision_ == revision

    all_tables = SQLite3Inspector().get_tables_names()
    assert len(all_tables) == 1


def test_get_revision_SQL_sqlite(make_database: str):
    SQLite3Config(make_database)
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
    SQLite3Executor.execute_sql(
        """
        CREATE TABLE test_table (id INTEGER, name TEXT);
        CREATE TABLE test_table_2 (idd INTEGER, count_ INTEGER, FOREIGN KEY (idd) REFERENCES test_table (id));
        INSERT INTO test_table (id, name) VALUES (1, 'test');
        """
    )
    manager = RevisionManager()
    revision = Revision(
        "test description",
        "test schema repr",
        DatabaseProvider.SQLITE3,
        [table_1, table_2],
    )
    revision_sql = manager.get_revision_SQL(revision)
    assert revision_sql == (
        "CREATE TABLE test_table (id INTEGER, name TEXT);\n"
        "CREATE TABLE test_table_2 (idd INTEGER, count_ INTEGER, FOREIGN KEY (idd) "
        "REFERENCES test_table (id));"
    )
