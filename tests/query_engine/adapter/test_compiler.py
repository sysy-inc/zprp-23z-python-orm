from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler
from skibidi_orm.query_engine.operations.crud import Insert, Update, Delete
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField
from skibidi_orm.query_engine.operations.select import Select
from skibidi_orm.query_engine.operations.functions import Count
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


def test_select_no_options():
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    st = Select(TestModel)
    compiler = SQLCompiler()
    correct_sql = "SELECT id, atr1, atr2 FROM TestModel ;"
    assert compiler.select(st) == correct_sql


def test_select_where_one_clause():
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    st = Select(TestModel).filter(id=1)
    compiler = SQLCompiler()
    correct_sql = "SELECT id, atr1, atr2 FROM TestModel WHERE id=1 ;"
    assert compiler.select(st) == correct_sql


def test_select_where_multiple_clause():
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    st = Select(TestModel).filter(id=1, atr1=2)
    compiler = SQLCompiler()
    correct_sql = "SELECT id, atr1, atr2 FROM TestModel WHERE id=1 AND atr1=2 ;"
    assert compiler.select(st) == correct_sql


def test_select_group_by():
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    st = Select(TestModel).group_by("id")
    compiler = SQLCompiler()
    correct_sql = "SELECT id FROM TestModel GROUP BY id ;"
    assert compiler.select(st) == correct_sql


def test_select_order_by():
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    st = Select(TestModel).order_by("id")
    compiler = SQLCompiler()
    correct_sql = "SELECT id, atr1, atr2 FROM TestModel ORDER BY id ;"
    assert compiler.select(st) == correct_sql


def test_select_order_by_desc():
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    st = Select(TestModel).order_by("id", desc=True)
    compiler = SQLCompiler()
    correct_sql = "SELECT id, atr1, atr2 FROM TestModel ORDER BY id DESC ;"
    assert compiler.select(st) == correct_sql


def test_select_alias():
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    st = Select(TestModel).annotate(my_id="id")
    compiler = SQLCompiler()
    correct_sql = "SELECT id AS my_id, atr1, atr2 FROM TestModel ;"
    assert compiler.select(st) == correct_sql


def test_select_count():
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    st = Select(TestModel).group_by("id").annotate(total=Count("id"))
    compiler = SQLCompiler()
    correct_sql = "SELECT id, COUNT(id) AS total FROM TestModel GROUP BY id ;"
    assert compiler.select(st) == correct_sql
