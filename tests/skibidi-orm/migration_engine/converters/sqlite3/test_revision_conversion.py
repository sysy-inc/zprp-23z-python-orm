def test_convert_revision_to_insertion_sql():
    from skibidi_orm.migration_engine.converters.sqlite3.all import SQLite3Converter
    from skibidi_orm.migration_engine.revisions.revision import Revision

    # The revisions are always created from snapshot objects, this is just for the case of testing the
    # SQL conversion.
    revision = Revision(
        timestamp="timestamp",
        description="description",
        schema_repr="test schema",
        provider="provider",
        schema_data=b"schema_data",
    )

    result = SQLite3Converter.convert_revision_to_insertion_sql(revision)

    assert result == (
        "INSERT INTO __revisions ("
        "timestamp, description, schema_repr, provider, schema_data)"
        " VALUES ('timestamp', 'description', 'test schema', 'provider', b'schema_data');"
    )
