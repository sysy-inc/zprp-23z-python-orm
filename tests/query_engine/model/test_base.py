from skibidi_orm.query_engine.field.field import CharField, IntegerField
from skibidi_orm.query_engine.model.base import Model

class Person(Model):
        name: str = CharField(default='Adam') # type: ignore
        age: int = IntegerField(default=30) # type: ignore


def test_creat_model():
    assert hasattr(Person, 'name')
    assert hasattr(Person, 'age')

def test_creat_person_args():
    person = Person('Mike', 21)
    assert person.name == 'Mike'
    assert person.age == 21

def test_creat_person_arg_and_kwarg():
    person = Person('Mike', age=21)
    assert person.name == 'Mike'
    assert person.age == 21

def test_creat_person_kwargs():
    person = Person(name='Mike', age=21)
    assert person.name == 'Mike'
    assert person.age == 21

def test_creat_person_default_and_arg():
    person = Person('Mike')
    assert person.name == 'Mike'
    assert person.age == 30

def test_creat_person_default_and_kwarg():
    person = Person(age=21)
    assert person.name == 'Adam'
    assert person.age == 21

def test_creat_person_both_default():
    person = Person()
    assert person.name == 'Adam'
    assert person.age == 30