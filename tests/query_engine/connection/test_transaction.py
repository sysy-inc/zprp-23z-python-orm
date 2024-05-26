from skibidi_orm.query_engine.connection.transaction import Transaction
from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler
from skibidi_orm.query_engine.operations.crud import Insert, Update, Delete
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def model_instance() -> Model:
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    return TestModel(1)

@pytest.fixture
def compiler_instance() -> SQLCompiler:
    return SQLCompiler()

@pytest.fixture
def connection_instance() -> MagicMock:
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = 1
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


def test_execute_insert_returning(compiler_instance: SQLCompiler, connection_instance: MagicMock, model_instance: Model):
    t = Transaction(compiler_instance, connection_instance[0])
    t.register_insert(model_instance)
    st = Insert(model_instance)
    t.execute_insert(st)
    connection_instance[0].cursor.assert_called_once()
    connection_instance[1].execute.assert_called_once_with("INSERT INTO test_model (id, atr1, atr2) VALUES (1, 1, 'a')RETURNING id;")
    connection_instance[1].fetchone.assert_called_once()


# def test_execute_insert_returning(compiler_instance: SQLCompiler, connection_instance: MagicMock, model_instance: Model):
#     t = Transaction(compiler_instance, connection_instance[0])
#     t.register_insert(model_instance)
#     st = Insert(model_instance)
#     t.execute_insert(st)
#     connection_instance[0].cursor.assert_called_once()
#     connection_instance[1].execute.assert_called_once_with("INSERT INTO test_model (id, atr1, atr2) VALUES (1, 1, 'a');")
#     connection_instance[1].fetchone.assert_not_called()


def test_execute_update(compiler_instance: SQLCompiler, connection_instance: MagicMock, model_instance: Model):
    t = Transaction(compiler_instance, connection_instance[0])
    t.register_update(model_instance)
    st = Update(model_instance)
    t.execute_update(st)
    connection_instance[0].cursor.assert_called_once()
    connection_instance[1].execute.assert_called_once_with("UPDATE test_model SET atr1=4 WHERE id=1;")


def test_execute_delete(compiler_instance: SQLCompiler, connection_instance: MagicMock, model_instance: Model):
    t = Transaction(compiler_instance, connection_instance[0])
    t.register_delete(model_instance)
    st = Delete(model_instance)
    t.execute_delete(st)
    connection_instance[0].cursor.assert_called_once()
    connection_instance[1].execute.assert_called_once_with("DELETE FROM test_model WHERE id=1;")
