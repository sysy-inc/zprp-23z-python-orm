from skibidi_orm.query_engine.field.field import CharField, IntegerField, AutoField
from skibidi_orm.query_engine.field.related_field import ForeignKey
from skibidi_orm.query_engine.model.base import Model
from typing import Optional
import pytest

class Person(Model):
    name: Optional[str | CharField] = CharField(default='Adam')
    age: Optional[int | IntegerField] = IntegerField(default=30)
    __db_table__ = 'person'

class Animal(Model):
    id: Optional[int | IntegerField] = IntegerField(primary_key=True)
    name: Optional[str | CharField] = CharField()

def test_create_model():
    assert hasattr(Person, 'name')
    assert hasattr(Person, 'age')
    assert hasattr(Person, 'person_id')
    assert hasattr(Person, '_meta')

def test_create_model_metaoptions_default_pimary_key():
    person = Person()
    assert hasattr(person._meta, 'db_table')
    assert hasattr(person._meta, 'local_fields')
    assert len(person._meta.local_fields) == 3
    assert hasattr(person._meta, 'meta')

def test_create_model_metaoptions_pimary_key_by_user():

    dog = Animal(1, 'Burek')
    assert hasattr(dog._meta, 'db_table')
    assert hasattr(dog._meta, 'local_fields')
    assert len(dog._meta.local_fields) == 2
    assert hasattr(dog._meta, 'meta')

def test_db_name_default():
    class Student(Model):
        idx: Optional [str| CharField] = CharField()
    student = Student('123123')
    assert  student._meta.db_table == 'student'

def test_db_name_by_user():
    person = Person()
    assert person._meta.db_table == 'person'

def test_two_pk_in_one_model():
    with pytest.raises(ValueError):
        class _(Model):
            id1: Optional[ int | IntegerField] = IntegerField(primary_key=True)
            id2: Optional[ int | AutoField] = AutoField(primary_key=True)

def test_get_primary_key_autofield():
    person = Person()
    assert person.person_id is None
    assert person.pk == person.person_id

def test_get_primary_key():
    dog = Animal(1, 'Reksio')
    assert dog.pk == dog.id

def test_set_primary_key_autofield():
    person = Person()
    person.pk = 1
    assert person.pk == 1

def test_set_primary_key():
    dog = Animal(1, 'Reksio')
    dog.pk = 2
    assert dog.pk == dog.id

def test_create_person_too_many_args():
    with pytest.raises(IndexError):
        Animal(1, 'Reksio', 1)

def test_create_person_args():
    person = Person('Mike', 21)
    assert person.name == 'Mike'
    assert person.age == 21
    assert person.person_id is None

def test_create_person_arg_and_kwarg():
    person = Person('Mike', age=21)
    assert person.name == 'Mike'
    assert person.age == 21

def test_create_person_kwargs():
    person = Person(name='Mike', age=21)
    assert person.name == 'Mike'
    assert person.age == 21

def test_create_person_default_and_arg():
    person = Person('Mike')
    assert person.name == 'Mike'
    assert person.age == 30

def test_create_person_default_and_kwarg():
    person = Person(age=21)
    assert person.name == 'Adam'
    assert person.age == 21

def test_create_person_both_default():
    person = Person()
    assert person.name == 'Adam'
    assert person.age == 30

class Owner(Model):
    id: Optional[int | IntegerField] = IntegerField(primary_key=True)
    name: Optional[str | CharField] = CharField()

class Dog(Model):
    id: Optional[int | IntegerField] = IntegerField(primary_key=True)
    name: Optional[str | CharField] = CharField('Reksio')
    owner: Optional[Owner | ForeignKey] = ForeignKey(to=Owner)

def test_create_foreign_key():
    adam = Owner(1, 'Adam')
    dog = Dog(1, "Reksio", adam)
    assert dog.owner == adam
    assert dog.owner_id == 1

def test_create_foreign_key_none():
    dog = Dog(1, "Reksio", None)
    assert dog.owner is None
    assert dog.owner_id is None

def test_create_foreign_key_by_id():
    dog = Dog(1, "Reksio", owner_id=2)
    with pytest.raises(ValueError):
        dog.owner

def test_set_foreign_key_obj():
    adam = Owner(1, "Adam")
    bolek = Owner(2, "Bolek")
    dog = Dog(1, "Reksio", adam)
    assert dog.owner == adam
    assert dog.owner_id == 1

    dog.owner = bolek
    assert dog.owner == bolek
    assert dog.owner_id == 2

def test_set_foreign_key_obj_id():
    adam = Owner(1, "Adam")     # TODO correct
    bolek = Owner(2, "Bolek")
    dog = Dog(1, "Reksio", adam)
    assert dog.owner == adam
    assert dog.owner_id == 1
    dog.owner_id = 2
    with pytest.raises(ValueError):
        dog.owner 

def test_set_foreign_key_from_none():
    adam = Owner(1, "Adam")
    dog = Dog(1, "Reksio", None)
    assert dog.owner is None
    assert dog.owner_id is None

    dog.owner = adam
    assert dog.owner == adam
    assert dog.owner_id == 1

def test_set_foreign_key_to_none():
    adam = Owner(1, "Adam")
    dog = Dog(1, "Reksio", adam)
    assert dog.owner == adam
    assert dog.owner_id == 1

    dog.owner = None
    assert dog.owner is None
    assert dog.owner_id is None

def test_set_foreign_key_id_to_none():
    adam = Owner(1, "Adam")
    dog = Dog(1, "Reksio", adam)
    assert dog.owner == adam
    assert dog.owner_id == 1

    dog.owner_id = None
    assert dog.owner is None
    assert dog.owner_id is None

def test_set_foreign_key_pk():
    adam = Owner(1, "Adam")
    dog = Dog(1, "Reksio", adam)
    assert dog.owner == adam
    assert dog.owner_id == 1

    adam.id = 2
    assert dog.owner == adam
    assert dog.owner_id == 2

def test_changes():
    adam = Owner(1, "Adam")
    adam.name = 'Jurek'
    assert adam._update_changes_db() == {'name': 'Jurek'}

def test_not_equal():
    bolek = Owner(1, 'Bolek')
    lolek = Owner(2, 'Lolek')
    assert bolek != lolek


def test_inheritance():
    class Item(Model):
        id : Optional[int | IntegerField] = IntegerField(primary_key=True)
        name: Optional[str | CharField] = CharField()

    class Box(Item):
        weight: Optional[int | IntegerField] = IntegerField()

    box = Box()
    assert len(box._meta.local_fields) == 3