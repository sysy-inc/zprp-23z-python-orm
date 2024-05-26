from skibidi_orm.query_engine.config import SQLiteConfig
from skibidi_orm.query_engine import config
from skibidi_orm.query_engine.connection.engine import Engine
from skibidi_orm.query_engine.adapter.sqlite_adapter import SQLiteAdapter
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_get_configuration(monkeypatch):
    def mock_config_data():
        return SQLiteConfig(path='test.db')

    mock_sqlite3 = MagicMock()
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [('row1', 'data1'), ('row2', 'data2')]
    mock_sqlite3.connect.return_value = mock_connection

    def mock_import_connector(self):
        self._connector = mock_sqlite3

    monkeypatch.setattr(config, 'get_configuration', mock_config_data)
    # monkeypatch.setattr('skibidi_orm.query_engine.adapter.sqlite_adapter.sqlite3', mock_sqlite3)
    monkeypatch.setattr(SQLiteAdapter, '_import_connector', mock_import_connector)

    return mock_sqlite3, mock_connection, mock_cursor


def test_create_engine(mock_get_configuration):
    engine = Engine()
    assert engine.connected is False


def test_connect(mock_get_configuration):
    engine = Engine()
    connection = engine.connect()
    assert connection is not None
    assert engine.connected is True


def test_close(mock_get_configuration):
    engine = Engine()
    engine.connect()
    assert engine.connected is True
    engine.close()
    assert engine.connected is False
