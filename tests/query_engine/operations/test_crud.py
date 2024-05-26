from skibidi_orm.query_engine.operations.crud import CRUDBase, ValueBase, Insert, Update, Delete
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField
import pytest

@pytest.fixture
def model_instance() -> Model:
    class TestModel(Model):
        id: int = IntegerField()  # type: ignore
    return TestModel(1)


def test_crudbase_creat(model_instance: Model):
    st = CRUDBase(model_instance)
    assert st.table() == "test_model"

# [("id", 1), ("atr1", 1), ("atr2", "a")]


def test_valuebase_values(model_instance: Model):
    st = ValueBase(model_instance)
    assert st.values() == [1, 1, "a"]


def test_valuebase_columns(model_instance: Model):
    st = ValueBase(model_instance)
    assert st.columns() == ["id", "atr1", "atr2"]


def test_valuebase_attributes(model_instance: Model):
    st = ValueBase(model_instance)
    assert st.attributes() == [("id", 1), ("atr1", 1), ("atr2", "a")]


def test_insert_returning(model_instance: Model):
    # model_instance is returning
    st = Insert(model_instance)
    assert st.returns is True
    assert st.returning_col == ["id"]


def test_insert_not_returning(model_instance: Model):
    # waiting for implementation in Model
    pass


def test_update(model_instance: Model):
    # TODO change model_instance attributes values model_instance.att = 2
    st = Update(model_instance)
    assert st.where_clause()[0].col == "id"
    assert st.where_clause()[0].val == 1


def test_delete(model_instance: Model):
    st = Delete(model_instance)
    assert st.where_clause()[0].col == "id"
    assert st.where_clause()[0].val == 1
