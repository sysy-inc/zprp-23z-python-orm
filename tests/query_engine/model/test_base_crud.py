from skibidi_orm.query_engine.field.related_field import ForeignKey
from skibidi_orm.query_engine.field.field import IntegerField
from skibidi_orm.query_engine.adapter.sqlite_adapter import SQLiteAdapter
from skibidi_orm.query_engine.connection.session import Session
from skibidi_orm.query_engine.connection.engine import Engine
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.config import SQLiteConfig
from skibidi_orm.query_engine import config
from typing import Optional, ForwardRef
import pytest
from unittest.mock import MagicMock


class PersonWithId(Model):
    id: Optional[ int| IntegerField ] = IntegerField(primary_key=True)
    age: Optional[ int | IntegerField ] = IntegerField()

class PersonWithoutId(Model):
    age: Optional[int | IntegerField ] = IntegerField()
    person: Optional[PersonWithId | ForeignKey] = ForeignKey(to=PersonWithId, on_delete='cos')

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

def test_create_model_foreign_key_the_same_model():
    StudentType: Optional['Student'] = ForwardRef('Student')
    class Student(Model):
        friend: Optional[StudentType | ForeignKey] = ForeignKey(to=PersonWithoutId, on_delete='cos')
    student1 = Student()
    student2 = Student(student1)
    assert student2.friend == student1

def test_get_realtion_field():
    person1 = PersonWithId(1, 23)
    person2 = PersonWithoutId(23, person1)
    assert person2._meta.get_relation_field("name") is None

def test_get_name_and_pk():
    person = PersonWithId(1, 2)
    assert person._get_name_and_pk() == ('personwithid', 1)

def test_get_name_and_pk_autofield():
    person1 = PersonWithId(1, 2)
    person2 = PersonWithoutId(2, person1)
    assert person2._get_name_and_pk() == ('personwithoutid', None)

def test_get_attr_values_without_none():
    person = PersonWithId(1, 2)
    assert person._get_attr_values() == [('id', 1), ('age', 2)]

def test_get_attr_values_with_none():
    person = PersonWithId(1)
    assert person._get_attr_values() == [('id', 1)]

def test_get_attr_values_foreign_key():
    person1 = PersonWithId(1)
    person2 = PersonWithoutId(2, person1)
    assert person2._get_attr_values() == [('age', 2), ('person_id', 1)]

def test_add_session(mock_get_configuration):
    person = PersonWithId(1)
    engine = Engine()
    session = Session(engine)
    person._add_session(session)
    assert hasattr(person, '_session')
    assert person._session == session

def test_remove_session(mock_get_configuration):
    person = PersonWithId(1)
    engine = Engine()
    session = Session(engine)
    person._add_session(session)
    assert hasattr(person, '_session')
    assert person._session == session

    person._remove_session()
    assert hasattr(person, '_session')
    assert person._session is None

def test_is_pk_none_false():
    person = PersonWithId(1, 22)
    assert person._is_pk_none() == False

def test_is_pk_none_true():
    person = PersonWithoutId(22)
    assert person._is_pk_none() == True

def test_get_db_pk():
    person = PersonWithId(1, 22)
    assert person._get_db_pk() == ('id', 1)