from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler
from skibidi_orm.query_engine.operations.crud import Insert, Update, Delete
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField
import pytest

@pytest.fixture
def model_instance() -> Model:
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    return TestModel(1)


def test_insert_returning(model_instance: Model):
    st = Insert(model_instance)
    compiler = SQLCompiler()
    correct_sql = "INSERT INTO test_model (id, atr1, atr2) VALUES (1, 1, 'a')RETURNING id;"
    assert compiler.insert(st) == correct_sql


def test_insert_no_returning():
    pass


def test_update(model_instance: Model):
    st = Update(model_instance)
    compiler = SQLCompiler()
    correct_sql = "UPDATE test_model SET atr1=4 WHERE id=1;"
    assert compiler.update(st) == correct_sql


def test_delete(model_instance: Model):
    st = Delete(model_instance)
    compiler = SQLCompiler()
    correct_sql = "DELETE FROM test_model WHERE id=1;"
    assert compiler.delete(st) == correct_sql
