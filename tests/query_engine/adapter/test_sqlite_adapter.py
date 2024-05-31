from skibidi_orm.query_engine.adapter.sqlite_adapter import SQLiteAdapter
import sqlite3


def test_create_SQLiteAdapter():
    adapter = SQLiteAdapter()
    assert adapter.connector is None


def test_make_connection():
    adapter = SQLiteAdapter()
    connection = adapter.make_connection(path=':memory:')
    assert connection is not None
    assert isinstance(connection, sqlite3.Connection)


def test_import_connector():
    adapter = SQLiteAdapter()
    assert adapter.connector is None
    # import_connector is private so it can't be used here directly
    # it is used during making connection
    adapter.make_connection(path=':memory:')
    assert adapter.connector == sqlite3
