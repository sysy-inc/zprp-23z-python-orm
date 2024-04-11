from skibidi_orm.query_engine.config import SQLiteConfig
from skibidi_orm.query_engine.connection.engine import Engine


def test_create_engine():
    config = SQLiteConfig(path='test.db')
    engine = Engine(config)
    assert engine.connected is False


def test_connect():
    config = SQLiteConfig(path='test.db')
    engine = Engine(config)
    connection = engine.connect()
    assert connection is not None
    assert engine.connected is True


def test_close():
    config = SQLiteConfig(path='test.db')
    engine = Engine(config)
    engine.connect()
    assert engine.connected is True
    engine.close()
    assert engine.connected is False
