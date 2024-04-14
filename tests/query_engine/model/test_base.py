from skibidi_orm.query_engine.field.field import CharField, IntegerField


def test_creat_model():
    class Person(base.Model):
        name: CharField
        age: IntegerField
    assert hasattr(Person, 'name')

def test_1():
    assert 1 == 1