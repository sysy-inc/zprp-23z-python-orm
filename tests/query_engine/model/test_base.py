from skibidi_orm.query_engine.field.field import CharField, IntegerField
from skibidi_orm.query_engine.model.base import Model
from typing import Optional

class Person(Model):
        name: Optional[str] = CharField(default='Adam')
        age: Optional[int] = IntegerField(default=30)

def test_create_model():
    assert hasattr(Person, 'name')
    assert hasattr(Person, 'age')
    assert hasattr(Person, '_meta')

def test_create_model_metadata():
    person = Person()
    assert hasattr(person, '_meta')
    assert hasattr(person._meta, 'db_table')
    assert hasattr(person._meta, 'local_fields')
    assert len(person._meta.local_fields) == 2

def test_create_person_args():
    person = Person('Mike', 21)
    assert person.name == 'Mike'
    assert person.age == 21

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