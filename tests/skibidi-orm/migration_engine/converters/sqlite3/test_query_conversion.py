from skibidi_orm.migration_engine.converters.sqlite3.queries import (
    SQLite3QueryConverter,
)
from skibidi_orm.migration_engine.revisions.constants import get_revision_table_name


def test_revision_data_query_according_to_get_revision_table_name():
    """Tests whether the get_revision_data_query contains the table name from get_revision_table_name"""
    assert (
        SQLite3QueryConverter.get_revision_data_query()
        == f"SELECT rowid, * FROM {get_revision_table_name()};"
    )


def test_table_clearing_query_according_to_get_revision_table_name():
    assert (
        SQLite3QueryConverter.get_table_clearing_query()
        == f"""
            PRAGMA writable_schema = 1;
            DELETE FROM sqlite_master WHERE type IN ('table', 'index', 'trigger') AND name != '{get_revision_table_name()}';
            PRAGMA writable_schema = 0;
            COMMIT;
            VACUUM;
            PRAGMA INTEGRITY_CHECK;
            """
    )
