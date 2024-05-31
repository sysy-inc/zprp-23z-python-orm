from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler
from skibidi_orm.query_engine.operations.crud import Insert, Update, Delete
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField, AutoField
from skibidi_orm.query_engine.operations.select import Select
from skibidi_orm.query_engine.operations.functions import Count
import pytest
from typing import Optional

@pytest.fixture
def model_instance() -> Model:
    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    return Person(1, 12)


def test_insert_no_returning(model_instance: Model):
    st = Insert(model_instance)
    compiler = SQLCompiler()
    correct_sql = "INSERT INTO person (id, age) VALUES (1, 12);"
    assert compiler.insert(st) == correct_sql


def test_insert_returning():
    class Person(Model):
        id: Optional[int | AutoField] = AutoField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()

    obj = Person(age=12)
    st = Insert(obj)
    compiler = SQLCompiler()
    correct_sql = "INSERT INTO person (age) VALUES (12)RETURNING id;"
    assert compiler.insert(st) == correct_sql


def test_update(model_instance: Model):
    model_instance.age = 4
    st = Update(model_instance)
    compiler = SQLCompiler()
    correct_sql = "UPDATE person SET age=4 WHERE id=1;"
    assert compiler.update(st) == correct_sql


def test_delete(model_instance: Model):
    st = Delete(model_instance)
    compiler = SQLCompiler()
    correct_sql = "DELETE FROM person WHERE id=1;"
    assert compiler.delete(st) == correct_sql


def test_select_no_options():
    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()
    st = Select(Person)
    compiler = SQLCompiler()
    correct_sql = "SELECT id, atr1, atr2 FROM person ;"
    assert compiler.select(st) == correct_sql


def test_select_where_one_clause():
    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()
    st = Select(Person).filter(id=1)
    compiler = SQLCompiler()
    correct_sql = "SELECT id, atr1, atr2 FROM person WHERE id=1 ;"
    assert compiler.select(st) == correct_sql


def test_select_where_multiple_clause():
    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()
    st = Select(Person).filter(id=1, atr1=2)
    compiler = SQLCompiler()
    correct_sql = "SELECT id, atr1, atr2 FROM person WHERE id=1 AND atr1=2 ;"
    assert compiler.select(st) == correct_sql


def test_select_group_by():
    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()
    st = Select(Person).group_by("id")
    compiler = SQLCompiler()
    correct_sql = "SELECT id FROM person GROUP BY id ;"
    assert compiler.select(st) == correct_sql


def test_select_order_by():
    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()
    st = Select(Person).order_by("id")
    compiler = SQLCompiler()
    correct_sql = "SELECT id, atr1, atr2 FROM person ORDER BY id ;"
    assert compiler.select(st) == correct_sql


def test_select_order_by_desc():
    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()
    st = Select(Person).order_by("id", desc=True)
    compiler = SQLCompiler()
    correct_sql = "SELECT id, atr1, atr2 FROM person ORDER BY id DESC ;"
    assert compiler.select(st) == correct_sql


def test_select_alias():
    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()
    st = Select(Person).annotate(my_id="id")
    compiler = SQLCompiler()
    correct_sql = "SELECT id AS my_id, atr1, atr2 FROM person ;"
    assert compiler.select(st) == correct_sql


def test_select_count():
    class Person(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        age: Optional[int | IntegerField] = IntegerField()
    st = Select(Person).group_by("id").annotate(total=Count("id"))
    compiler = SQLCompiler()
    correct_sql = "SELECT id, COUNT(id) AS total FROM person GROUP BY id ;"
    assert compiler.select(st) == correct_sql
