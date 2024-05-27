from skibidi_orm.query_engine.field.field import IntegerField
from skibidi_orm.query_engine.field.related_field import ForeignKey
from skibidi_orm.query_engine.model.base import Model
from typing import Optional


class PersonWithId(Model):
    id: Optional[ int| IntegerField ] = IntegerField(primary_key=True)
    age: Optional[ int | IntegerField ] = IntegerField()

class PersonWithoutId(Model):
    age: Optional[int | IntegerField ] = IntegerField()
    person: Optional[PersonWithId | ForeignKey] = ForeignKey(to=PersonWithId, on_delete='cos')


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