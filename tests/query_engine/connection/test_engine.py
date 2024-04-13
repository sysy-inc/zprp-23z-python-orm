from skibidi_orm.query_engine.config import SQLiteConfig
from skibidi_orm.query_engine import config
from skibidi_orm.query_engine.connection.engine import Engine
import pytest


@pytest.fixture
def mock_get_configuration(monkeypatch):
    def mock_config_data():
        return SQLiteConfig(path='test.db')

    monkeypatch.setattr(config, 'get_configuration', mock_config_data)


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
