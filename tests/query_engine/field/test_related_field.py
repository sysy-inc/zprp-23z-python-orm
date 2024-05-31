import pytest
from skibidi_orm.query_engine.field.related_field import ForeignKey
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.field.field import CharField
from typing import Optional


def test_ForeignKey_fromModel():
    class Animal(Model):
        name: Optional[str | CharField] = CharField(default='Adam')

    class Person(Model):
        name: Optional[str | CharField] = CharField(default='Adam')
        friend = ForeignKey(to=Animal, default=None)

    adam = Animal()
    basia = Person(name='Basia', friend=adam)
    assert basia.friend is not None
