from skibidi_orm.query_engine.config import SQLiteConfig
from skibidi_orm.query_engine.connection.engine import Engine
from skibidi_orm.query_engine.connection.session import Session
from skibidi_orm.query_engine import config
import pytest


@pytest.fixture
def mock_get_configuration(monkeypatch):
    def mock_config_data():
        return SQLiteConfig(path='test.db')

    monkeypatch.setattr(config, 'get_configuration', mock_config_data)


def test_create_session(mock_get_configuration):
    engine = Engine()
    session = Session(engine)
    assert session.connection is None


def test_enter_exit(mock_get_configuration):
    engine = Engine()
    with Session(engine) as session:
        assert session.connection is not None
    assert session.connection is None


def test_close(mock_get_configuration):
    engine = Engine()
    with Session(engine) as session:
        session.close()
    assert session.connection is None
