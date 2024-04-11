from skibidi_orm.query_engine.config import SQLiteConfig
from skibidi_orm.query_engine.adapter.sqlite_adapter import SQLiteAdapter


def test_create_SQLiteConfig():
    config = SQLiteConfig(path='test.db')
    assert config.adapter is not None
    assert isinstance(config.adapter, SQLiteAdapter)


def test_connection_data():
    config = SQLiteConfig(path='test.db')
    data = config.connection_data()
    assert data == {'path': 'test.db'}
