from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.revisions.manager import RevisionManager


def test_create_and_find_revision_table_sqlite(make_database: str):
    """Tests whether the revision table is found if it does not exist"""
    SQLite3Config(make_database)
    manager = RevisionManager()
    assert not manager.find_revision_table()
    manager.create_revision_table()
    assert manager.find_revision_table()
