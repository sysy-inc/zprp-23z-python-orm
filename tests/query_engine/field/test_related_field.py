from skibidi_orm.query_engine.field.related_field import ForeignKey
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import CharField, IntegerField
from typing import Optional, ForwardRef


def test_ForeignKey_anotherModel():
    class Owner(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        name: Optional[str | CharField] = CharField()

    class Dog(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        name: Optional[str | CharField] = CharField('Reksio')
        owner: Optional[Owner | ForeignKey] = ForeignKey(to=Owner)

    adam = Owner(1, 'Adam')
    dog = Dog(1, "Reksio", adam)
    assert dog.owner == adam
    assert dog.owner_id == 1


def test_ForeignKey_self():
    DogType: Optional['Dog'] = ForwardRef('Dog')
    class Dog(Model):
        id: Optional[int | IntegerField] = IntegerField(primary_key=True)
        name: Optional[str | CharField] = CharField('Reksio')
        friend: Optional[DogType | ForeignKey] = ForeignKey(to='self')

    maks = Dog(1, 'Maks')
    reks = Dog(2, "Reks", maks)
    assert reks.friend == maks

