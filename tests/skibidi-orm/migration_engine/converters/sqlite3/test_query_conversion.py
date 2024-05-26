from skibidi_orm.migration_engine.converters.sqlite3.queries import (
    SQLite3QueryConverter,
)


def test_revision_data_query():
    assert (
        SQLite3QueryConverter.convert_get_revision_data_query()
        == "SELECT * FROM __revisions;"
    )
