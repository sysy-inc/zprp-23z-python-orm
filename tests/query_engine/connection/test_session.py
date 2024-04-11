from skibidi_orm.query_engine.config import SQLiteConfig
from skibidi_orm.query_engine.connection.engine import Engine
from skibidi_orm.query_engine.connection.session import Session


def test_create_session():
    config = SQLiteConfig(path='test.db')
    engine = Engine(config)
    session = Session(engine)
    assert session.connection is None


def test_enter_exit():
    config = SQLiteConfig(path='test.db')
    engine = Engine(config)
    with Session(engine) as session:
        assert session.connection is not None
    assert session.connection is None


def test_close():
    config = SQLiteConfig(path='test.db')
    engine = Engine(config)
    with Session(engine) as session:
        session.close()
    assert session.connection is None
