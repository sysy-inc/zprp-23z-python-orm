from skibidi_orm.migration_engine.converters.sqlite3.queries import (
    SQLite3QueryConverter,
)


def test_revision_data_query():
    assert (
        SQLite3QueryConverter.get_revision_data_query()
        == "SELECT rowid, * FROM __revisions;"
    )


def test_table_clearing_query():
    assert (
        SQLite3QueryConverter.get_table_clearing_query()
        == """
            PRAGMA writable_schema = 1;
            DELETE FROM sqlite_master WHERE type IN ('table', 'index', 'trigger') AND name != '__revisions';
            PRAGMA writable_schema = 0;
            COMMIT;
            VACUUM;
            PRAGMA INTEGRITY_CHECK;
            """
    )
