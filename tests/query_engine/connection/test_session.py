from skibidi_orm.query_engine.config import SQLiteConfig
from skibidi_orm.query_engine.connection.engine import Engine
from skibidi_orm.query_engine.connection.session import Session
from skibidi_orm.query_engine import config
from skibidi_orm.query_engine.adapter.sqlite_adapter import SQLiteAdapter
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField, AutoField
from skibidi_orm.query_engine.field.related_field import ForeignKey
from skibidi_orm.query_engine.operations.select import Select
from skibidi_orm.query_engine.connection.result import Result
import pytest
from unittest.mock import MagicMock
from typing import Optional


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

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1


def test_changed(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        session.changed(obj)        # TODO change
        assert len(session._new) == 1


def test_changed_already_marked_changed(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        session.changed(obj)    # TODO change
        assert len(session._new) == 1
        session.changed(obj)    # TODO
        # nothing happens
        assert len(session._new) == 1


def test_changed_marked_delete(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        session.delete(obj)
        session.changed(obj)    # TODO
        # nothing happens
        assert len(session._new) == 0


def test_changed_not_added_to_session(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.changed(obj)    # TODO
        # nothing happens
        assert len(session._new) == 0


def test_delete_object_not_in_new(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        # object added to databes and to IdentityMap
        session.delete(obj)
        assert len(session._delete) == 1


def test_delete_object_in_new(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        # object not inserted yet
        session.delete(obj)
        assert len(session._delete) == 0
        assert len(session._new) == 0


def test_delete_object_in_new_in_dirty(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        # object not inserted yet
        session.changed(obj)    # TODO
        assert len(session._dirty) == 1
        session.delete(obj)
        assert len(session._delete) == 0
        assert len(session._new) == 0
        assert len(session._dirty) == 0


def test_delete_object_not_in_new_in_dirty(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        session.commit()
        # object added to databes and to IdentityMap
        session.changed(obj)    # TODO
        assert len(session._dirty) == 1
        session.delete(obj)
        assert len(session._delete) == 1
        assert len(session._dirty) == 0


def test_delete_object_not_in_session(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
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

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        session.flush()
        assert len(session._new) == 0
        assert len(session._map) == 1
        mock_get_configuration[2].execute.assert_called()


def test_flush_update_pending(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        session.flush()
        session.changed(obj)    # TODO
        assert len(session._dirty) == 1
        session.flush()
        assert len(session._dirty) == 0
        mock_get_configuration[2].execute.assert_called()


def test_flush_delete_pending(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        session.flush()
        session.delete(obj)
        assert len(session._delete) == 1
        session.flush()
        assert len(session._delete) == 0
        mock_get_configuration[2].execute.assert_called()


def test_flush_insert_pending_relation_no_key(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    class Dog(Model):
        id_dog: Optional[int | IntegerField] = IntegerField(primary_key=True)
        owner: Optional[Person | ForeignKey] = ForeignKey(to=Person)

    p = Person(1, 12)
    d = Dog(1)

    with Session(engine) as session:
        session.add(d)
        session.add(p)
        with pytest.raises(Exception):
            session.flush()


def test_flush_insert_pending_relation_object_not_in_map_processed(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    class Dog(Model):
        id_dog: Optional[int | IntegerField] = IntegerField(primary_key=True)
        owner: Optional[Person | ForeignKey] = ForeignKey(to=Person)

    p = Person(1, 12)
    d = Dog(1, owner=p)
    with Session(engine) as session:
        session.add(p)
        session.add(d)
        assert len(session._new) == 2
        session.flush()
        assert len(session._new) == 0
        assert len(session._map) == 2
        mock_get_configuration[2].execute.assert_called()


def test_flush_insert_pending_relation_object_not_in_map_not_processed(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    class Dog(Model):
        id_dog: Optional[int | IntegerField] = IntegerField(primary_key=True)
        owner: Optional[Person | ForeignKey] = ForeignKey(to=Person)

    p = Person(1, 12)
    d = Dog(1, owner=p)
    with Session(engine) as session:
        session.add(d)
        session.add(p)
        assert len(session._new) == 2
        session.flush()
        assert len(session._new) == 0
        assert len(session._map) == 2
        mock_get_configuration[2].execute.assert_called()


def test_flush_insert_pending_relation_object_in_map(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    class Dog(Model):
        id_dog: Optional[int | IntegerField] = IntegerField(primary_key=True)
        owner: Optional[Person | ForeignKey] = ForeignKey(to=Person)

    p = Person(1, 12)
    d = Dog(1, owner=p)
    with Session(engine) as session:
        session.add(p)
        session.commit()
        session.add(d)
        assert len(session._new) == 1
        session.flush()
        assert len(session._new) == 0
        assert len(session._map) == 2
        mock_get_configuration[2].execute.assert_called()


def test_flush_insert_pending_relation_id_in_map(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    class Dog(Model):
        id_dog: Optional[int | IntegerField] = IntegerField(primary_key=True)
        owner: Optional[Person | ForeignKey] = ForeignKey(to=Person)

    p = Person(1, 12)
    d = Dog(1, owner_id=1)
    with Session(engine) as session:
        session.add(p)
        session.commit()
        session.add(d)
        assert len(session._new) == 1
        session.flush()
        assert len(session._new) == 0
        assert len(session._map) == 2
        mock_get_configuration[2].execute.assert_called()


def test_flush_insert_pending_relation_id_not_in_map_in_new(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    class Dog(Model):
        id_dog: Optional[int | IntegerField] = IntegerField(primary_key=True)
        owner: Optional[Person | ForeignKey] = ForeignKey(to=Person)

    p = Person(1, 12)
    d = Dog(1, owner_id=1)
    with Session(engine) as session:
        session.add(d)
        session.add(p)
        assert len(session._new) == 2
        session.flush()
        assert len(session._new) == 0
        assert len(session._map) == 2
        mock_get_configuration[2].execute.assert_called()


def test_select_return_model(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    st = Select(Person)
    mock_get_configuration[2].fetchall.return_value = [(1, 12)]
    mock_get_configuration[2].description = [["id"]]

    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        ret = session.select(st)
        mock_get_configuration[2].execute.assert_called()
        assert len(ret) == 1
        assert ret[0].id == 1
        assert isinstance(ret[0], Person)


def test_select_return_result(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    st = Select(Person).group_by("id")
    mock_get_configuration[2].fetchall.return_value = [(1,)]
    mock_get_configuration[2].description = [["id"]]

    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        ret = session.select(st)
        mock_get_configuration[2].execute.assert_called()
        assert len(ret) == 1
        assert ret[0].id == 1
        assert isinstance(ret[0], Result)


def test_get(mock_get_configuration):
    engine = Engine()

    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(1, 12)
    st = Select(Person)
    mock_get_configuration[2].fetchall.return_value = [(1, 12)]
    mock_get_configuration[2].description = [["id"]]

    with Session(engine) as session:
        session.add(obj)
        assert len(session._new) == 1
        ret = session.get(Person, 1)
        mock_get_configuration[2].execute.assert_called()
        assert ret.id == 1
        assert isinstance(ret, Person)
