from skibidi_orm.query_engine.operations.crud import CRUDBase, ValueBase, Insert, Update, Delete
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField, AutoField
from skibidi_orm.query_engine.connection.engine import Engine
from skibidi_orm.query_engine.connection.session import Session
from skibidi_orm.query_engine.config import SQLiteConfig, SQLiteAdapter
from skibidi_orm.query_engine import config
import pytest
from typing import Optional
from unittest.mock import MagicMock

@pytest.fixture
def model_instance() -> Model:
    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    return Person(1, 12)

@pytest.fixture
def mock_get_configuration(monkeypatch):
    def mock_config_data():
        return SQLiteConfig(path='test.db')

    mock_sqlite3 = MagicMock()

    def mock_import_connector(self):
        self._connector = mock_sqlite3

    monkeypatch.setattr(config, 'get_configuration', mock_config_data)
    monkeypatch.setattr(SQLiteAdapter, '_import_connector', mock_import_connector)

    return mock_sqlite3


def test_crudbase_creat(model_instance: Model):
    st = CRUDBase(model_instance)
    assert st.table() == "person"


def test_valuebase_values(model_instance: Model):
    st = ValueBase(model_instance)
    assert st.values() == [1, 12]


def test_valuebase_columns(model_instance: Model):
    st = ValueBase(model_instance)
    assert st.columns() == ["id", "age"]


def test_valuebase_attributes(model_instance: Model):
    st = ValueBase(model_instance)
    assert st.attributes() == [("id", 1), ("age", 12)]


def test_insert_returning(model_instance: Model):
    st = Insert(model_instance)
    assert st.returns is False
    assert st.returning_col == []


def test_insert_not_returning(model_instance: Model):
    class Person(Model):
        id: Optional[int | AutoField] = AutoField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()
    obj = Person(age=12)
    st = Insert(obj)
    assert st.returns is True
    assert st.returning_col == ["id"]


def test_update(model_instance: Model, mock_get_configuration):
    eng = Engine()
    with Session(eng) as session:
        session.add(model_instance)
        model_instance.age = 4
        st = Update(model_instance)
        assert st.attributes() == [("age", 4)]
        assert st.where_clause()[0].col == "id"
        assert st.where_clause()[0].val == 1


def test_delete(model_instance: Model):
    st = Delete(model_instance)
    assert st.where_clause()[0].col == "id"
    assert st.where_clause()[0].val == 1
