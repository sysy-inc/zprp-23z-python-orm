from skibidi_orm.query_engine.operations.select import Select
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField
from skibidi_orm.query_engine.operations import clauses as c
import pytest


class TestModel(Model):
    id: int = IntegerField()  # type: ignore


def test_creat():
    st = Select(TestModel)
    assert st.model == TestModel
    assert st.fields == ["id", "atr1", "atr2"]
    assert len(st.where_clauses) == 0
    assert len(st.group_by_col) == 0
    assert len(st.order_by_col[0]) == 0
    assert st.order_by_col[1] is False
    assert st.returning_model is True
    assert len(st.annotations) == 0


def test_filter_equal():
    st = Select(TestModel).filter(id=1)
    assert len(st.where_clauses) == 1
    assert st.where_clauses[0].col == "id"
    assert st.where_clauses[0].val == 1
    assert st.where_clauses[0].type == c.Eq


def test_filter_greater_than():
    st = Select(TestModel).filter(id__gt=1)
    assert len(st.where_clauses) == 1
    assert st.where_clauses[0].col == "id"
    assert st.where_clauses[0].val == 1
    assert st.where_clauses[0].type == c.Gt


def test_filter_greater_than_equal():
    st = Select(TestModel).filter(id__gte=1)
    assert len(st.where_clauses) == 1
    assert st.where_clauses[0].col == "id"
    assert st.where_clauses[0].val == 1
    assert st.where_clauses[0].type == c.GtEq


def test_filter_lower_than():
    st = Select(TestModel).filter(id__lt=1)
    assert len(st.where_clauses) == 1
    assert st.where_clauses[0].col == "id"
    assert st.where_clauses[0].val == 1
    assert st.where_clauses[0].type == c.Lt


def test_filter_lower_than_equal():
    st = Select(TestModel).filter(id__lte=1)
    assert len(st.where_clauses) == 1
    assert st.where_clauses[0].col == "id"
    assert st.where_clauses[0].val == 1
    assert st.where_clauses[0].type == c.LtEq


def test_filter_not_equal():
    st = Select(TestModel).filter(id__not=1)
    assert len(st.where_clauses) == 1
    assert st.where_clauses[0].col == "id"
    assert st.where_clauses[0].val == 1
    assert st.where_clauses[0].type == c.NotEq


def test_filter_is_Null():
    st = Select(TestModel).filter(id__isnull=True)
    assert len(st.where_clauses) == 1
    assert st.where_clauses[0].col == "id"
    assert st.where_clauses[0].val is None
    assert st.where_clauses[0].type == c.Null


def test_filter_is_not_Null():
    st = Select(TestModel).filter(id__isnull=False)
    assert len(st.where_clauses) == 1
    assert st.where_clauses[0].col == "id"
    assert st.where_clauses[0].val is None
    assert st.where_clauses[0].type == c.NotNull


def test_filter_unknown_option():
    with pytest.raises(SyntaxError):
        Select(TestModel).filter(id__unknown=3)


def test_group_by():
    st = Select(TestModel).group_by("id")
    assert len(st.group_by_col) == 1
    assert st.group_by_col[0] == "id"
    assert len(st.fields) == 1
    assert st.fields[0] == "id"
    assert st.returning_model is False


def test_group_by_with_annotations():
    st = Select(TestModel).annotate(my_name="atr1").group_by("id")
    assert len(st.annotations) != 0
    assert len(st.group_by_col) == 1
    assert st.group_by_col[0] == "id"
    assert len(st.fields) == 2
    assert "atr1" in st.fields
    assert "id" in st.fields
    assert st.returning_model is False


def test_group_by_annotate_group_by_col():
    st = Select(TestModel).annotate(my_id="id").group_by("id")
    assert len(st.annotations) != 0
    assert len(st.group_by_col) == 1
    assert st.group_by_col[0] == "id"
    assert len(st.fields) == 1
    assert st.fields[0] == "id"
    assert st.returning_model is False


def test_annotate():
    st = Select(TestModel).annotate(my_id="id")
    assert len(st.annotations) == 1
    assert len(st.fields) == 3
    assert st.annotations["id"] == "my_id"


def test_annotate_new_col():
    st = Select(TestModel).annotate(my_name="name")
    assert len(st.annotations) == 1
    assert len(st.fields) == 4
    assert st.annotations["name"] == "my_name"


def test_order_by():
    st = Select(TestModel).order_by("id")
    assert len(st.order_by_col[0]) == 1
    assert st.order_by_col[1] is False


def test_order_by_desc():
    st = Select(TestModel).order_by("id", desc=True)
    assert len(st.order_by_col[0]) == 1
    assert st.order_by_col[1] is True
