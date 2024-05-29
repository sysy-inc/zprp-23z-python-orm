from skibidi_orm.migration_engine.adapters.database_objects.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.adapters.providers import DatabaseProvider
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.revisions.manager import RevisionManager
from skibidi_orm.migration_engine.revisions.revision import Revision


def test_create_and_find_revision_table_sqlite(make_database: str):
    """Tests whether the revision table is found if it does not exist"""
    SQLite3Config(make_database)
    manager = RevisionManager()
    assert not manager.find_revision_table()
    manager.create_revision_table()
    assert manager.find_revision_table()


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
