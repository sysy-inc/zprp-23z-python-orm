from skibidi_orm.query_engine.connection.transaction import Transaction
from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler
from skibidi_orm.query_engine.operations.crud import Insert, Update, Delete
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField, AutoField
from skibidi_orm.query_engine.connection.engine import Engine
from skibidi_orm.query_engine.connection.session import Session
from skibidi_orm.query_engine.config import SQLiteConfig, SQLiteAdapter
from skibidi_orm.query_engine import config
import pytest
from unittest.mock import MagicMock
from typing import Optional

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

@pytest.fixture
def compiler_instance() -> SQLCompiler:
    return SQLCompiler()

@pytest.fixture
def connection_instance() -> MagicMock:
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = (1,)
    return (mock_connection, mock_cursor)


def test_creat_transaction(compiler_instance: SQLCompiler, connection_instance: MagicMock):
    t = Transaction(compiler_instance, connection_instance[0])
    assert len(t.insert_list) == 0
    assert len(t.update_list) == 0
    assert len(t.delete_list) == 0


def test_register_insert(compiler_instance: SQLCompiler, connection_instance: MagicMock, model_instance: Model):
    t = Transaction(compiler_instance, connection_instance[0])
    assert len(t.insert_list) == 0
    assert len(t.update_list) == 0
    assert len(t.delete_list) == 0
    t.register_insert(model_instance)
    assert len(t.insert_list) == 1
    assert len(t.update_list) == 0
    assert len(t.delete_list) == 0


def test_register_update(compiler_instance: SQLCompiler, connection_instance: MagicMock, model_instance: Model):
    t = Transaction(compiler_instance, connection_instance[0])
    assert len(t.insert_list) == 0
    assert len(t.update_list) == 0
    assert len(t.delete_list) == 0
    t.register_update(model_instance)
    assert len(t.insert_list) == 0
    assert len(t.update_list) == 1
    assert len(t.delete_list) == 0


def test_register_delete(compiler_instance: SQLCompiler, connection_instance: MagicMock, model_instance: Model):
    t = Transaction(compiler_instance, connection_instance[0])
    assert len(t.insert_list) == 0
    assert len(t.update_list) == 0
    assert len(t.delete_list) == 0
    t.register_delete(model_instance)
    assert len(t.insert_list) == 0
    assert len(t.update_list) == 0
    assert len(t.delete_list) == 1


def test_execute_insert_not_returning(compiler_instance: SQLCompiler, connection_instance: MagicMock, model_instance: Model):
    t = Transaction(compiler_instance, connection_instance[0])
    t.register_insert(model_instance)
    st = Insert(model_instance)
    t.execute_insert(st)
    connection_instance[0].cursor.assert_called_once()
    connection_instance[1].execute.assert_called_once_with("INSERT INTO person (id, age) VALUES (1, 12);")


def test_execute_insert_returning(compiler_instance: SQLCompiler, connection_instance: MagicMock):
    class Person(Model):
        id: Optional[int | AutoField] = AutoField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()
    obj = Person(age=12)
    t = Transaction(compiler_instance, connection_instance[0])
    t.register_insert(obj)
    st = Insert(obj)
    t.execute_insert(st)
    connection_instance[0].cursor.assert_called_once()
    connection_instance[1].execute.assert_called_once_with("INSERT INTO person (age) VALUES (12)RETURNING id;")
    connection_instance[1].fetchone.assert_called_once()
    assert obj.pk == 1


def test_execute_update(compiler_instance: SQLCompiler, connection_instance: MagicMock, model_instance: Model, mock_get_configuration):
    eng = Engine()
    with Session(eng) as session:
        session.add(model_instance)
        t = Transaction(compiler_instance, connection_instance[0])
        model_instance.age = 4
        st = Update(model_instance)
        t.execute_update(st)
        connection_instance[0].cursor.assert_called_once()
        connection_instance[1].execute.assert_called_once_with("UPDATE person SET age=4 WHERE id=1;")


def test_execute_delete(compiler_instance: SQLCompiler, connection_instance: MagicMock, model_instance: Model):
    t = Transaction(compiler_instance, connection_instance[0])
    t.register_delete(model_instance)
    st = Delete(model_instance)
    t.execute_delete(st)
    connection_instance[0].cursor.assert_called_once()
    connection_instance[1].execute.assert_called_once_with("DELETE FROM person WHERE id=1;")
