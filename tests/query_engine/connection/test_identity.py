from skibidi_orm.query_engine.connection.identity import IdentityMap
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import IntegerField
import pytest

@pytest.fixture
def model_instance() -> Model:
    class TestModel(Model):
        id: int = IntegerField(primary_key=True)  # type: ignore
    return TestModel(1)


def test_creat_IdentityMap():
    map = IdentityMap()
    assert len(map) == 0


def test_add(model_instance: Model):
    map = IdentityMap()
    assert len(map) == 0
    map.add(model_instance)
    assert len(map) == 1


def test_add_already_saved(model_instance: Model):
    map = IdentityMap()
    assert len(map) == 0
    map.add(model_instance)
    assert len(map) == 1
    # try to save it again
    map.add(model_instance)
    # nothing happens
    assert len(map) == 1


def test_add_key_already_present(model_instance: Model):
    class TestModel(Model):
        id: int = IntegerField(primary_key=True)  # type: ignore
    different_model_instance = TestModel(1)
    map = IdentityMap()
    assert len(map) == 0
    map.add(model_instance)
    assert len(map) == 1
    with pytest.raises(Exception):
        map.add(different_model_instance)


def test_get(model_instance: Model):
    map = IdentityMap()
    assert len(map) == 0
    map.add(model_instance)
    assert len(map) == 1
    model = map.get(("testmodel", 1))
    assert model == model_instance


def test_get_default():
    map = IdentityMap()
    assert len(map) == 0
    # there is no object with this key
    model = map.get(("testmodel", 1))
    assert model is None


def test_get_default_given(model_instance: Model):
    map = IdentityMap()
    assert len(map) == 0
    # there is no object with this key
    model = map.get(("testmodel", 1), model_instance)
    assert model == model_instance


def test_remove(model_instance: Model):
    map = IdentityMap()
    assert len(map) == 0
    map.add(model_instance)
    assert len(map) == 1
    map.remove(model_instance)
    assert len(map) == 0


def test_remove_the_same_key_different_instance(model_instance: Model):
    class TestModel(Model):
        id: int = IntegerField(primary_key=True)  # type: ignore
    different_model_instance = TestModel(1)
    map = IdentityMap()
    assert len(map) == 0
    map.add(model_instance)
    assert len(map) == 1
    # they have the same key
    assert different_model_instance._get_name_and_pk() == model_instance._get_name_and_pk()
    map.remove(different_model_instance)
    # nothing happens
    assert len(map) == 1


def test_remove_not_in_map(model_instance: Model):
    map = IdentityMap()
    assert len(map) == 0
    map.remove(model_instance)
    # nothing happens
    assert len(map) == 0
