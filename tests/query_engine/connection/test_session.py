from skibidi_orm.query_engine.config import SQLiteConfig
from skibidi_orm.query_engine.connection.engine import Engine
from skibidi_orm.query_engine.connection.session import Session
from skibidi_orm.query_engine import config
from skibidi_orm.query_engine.adapter.sqlite_adapter import SQLiteAdapter
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField
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
    mock_connection.rollback = MagicMock()
    mock_connection.commit = MagicMock()
    mock_cursor.fetchone.return_value = 1
    mock_sqlite3.connect.return_value = mock_connection

    def mock_import_connector(self):
        self._connector = mock_sqlite3

    monkeypatch.setattr(config, 'get_configuration', mock_config_data)
    # monkeypatch.setattr('skibidi_orm.query_engine.adapter.sqlite_adapter.sqlite3', mock_sqlite3)
    monkeypatch.setattr(SQLiteAdapter, '_import_connector', mock_import_connector)

    return mock_sqlite3, mock_connection, mock_cursor


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
    mock_get_configuration[1].rollback.assert_called_once()


def test_rollback(mock_get_configuration):
    mock_sqlite3, mock_connection, mock_cursor = mock_get_configuration
    engine = Engine()
    with Session(engine) as session:
        assert session.connection is not None
        session.rollback()
        mock_connection.rollback.assert_called_once()


def test_commit(mock_get_configuration):
    mock_sqlite3, mock_connection, mock_cursor = mock_get_configuration
    engine = Engine()
    with Session(engine) as session:
        assert session.connection is not None
        session.commit()
        mock_connection.commit.assert_called_once()


def test_add(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1


def test_changed(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        session.changed(obj)
        assert len(session._new) == 1


def test_changed_already_marked_changed(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        session.changed(obj)
        assert len(session._new) == 1
        session.changed(obj)
        # nothing happens
        assert len(session._new) == 1


def test_changed_marked_delete(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        session.delete(obj)
        session.changed(obj)
        # nothing happens
        assert len(session._new) == 0


def test_changed_not_added_to_session(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.changed(obj)
        # nothing happens
        assert len(session._new) == 0


def test_delete_object_not_in_new(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        # object added to databes and to IdentityMap
        session.delete(obj)
        assert len(session._delete) == 1


def test_delete_object_in_new(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        # object not inserted yet
        session.delete(obj)
        assert len(session._delete) == 0
        assert len(session._new) == 0


def test_delete_object_in_new_in_dirty(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        # object not inserted yet
        session.changed(obj)
        assert len(session._dirty) == 1
        session.delete(obj)
        assert len(session._delete) == 0
        assert len(session._new) == 0
        assert len(session._dirty) == 0


def test_delete_object_not_in_new_in_dirty(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        # object added to databes and to IdentityMap
        session.changed(obj)
        assert len(session._dirty) == 1
        session.delete(obj)
        assert len(session._delete) == 1
        assert len(session._dirty) == 0


def test_delete_object_not_in_session(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        with pytest.raises(ValueError):
            session.delete(obj)


def test_flush_clear(mock_get_configuration):
    engine = Engine()

    with Session(engine) as session:
        session.flush()
        # no sql executed
        mock_get_configuration[2].execute.assert_not_called()


def test_flush_insert_pending(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        session.flush()
        assert len(session._new) == 0
        assert len(session._map) == 1
        mock_get_configuration[2].execute.assert_called()


def test_flush_update_pending(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        session.flush()
        session.changed(obj)
        assert len(session._dirty) == 1
        session.flush()
        assert len(session._dirty) == 0
        mock_get_configuration[2].execute.assert_called()


def test_flush_delete_pending(mock_get_configuration):
    engine = Engine()

    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    obj = TestModel(1)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        session.flush()
        session.delete(obj)
        assert len(session._delete) == 1
        session.flush()
        assert len(session._delete) == 0
        mock_get_configuration[2].execute.assert_called()