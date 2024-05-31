======================
Model
======================

How to create your own model?
===============================

Welcome to skibidi project! You can create a database model with our library with us.

Every model should enherit from 'Model'.

Example
-------


.. code-block:: python

  from skibidi_orm.query_engine.field.field import CharField, IntegerField
  from skibidi_orm.query_engine.model.base import Model
  from typing import Optional

  class Person(Model):
    name: Optional[str | CharField] = CharField(default='Adam')
    age: Optional[int | IntegerField] = IntegerField(default=30)
    __db_table__ = 'person'

  person = Person('Ada', 23)


Attribut *__db_table__* is a name of table in database. It is not neccesary. Another attributs are mapping to the column of table. You can add attributs in this way: *'attr_name: Optional[python_type | Field] = Field()'*. You can define primary key, use the *AutoField* or do not define it, because skibidi can do this for you.

Inheritance
-----------
You can inherit after your own models.

.. code-block:: python

  from skibidi_orm.query_engine.field.field import CharField, IntegerField
  from skibidi_orm.query_engine.model.base import Model
  from typing import Optional

  class Item(Model):
      id : Optional[int | IntegerField] = IntegerField(primary_key=True)
      name: Optional[str | CharField] = CharField()

  class Box(Item):
      weight: Optional[int | IntegerField] = IntegerField()

  box = Box(1, 'basket', 15)

Foreign Key
------------

You can also create your foreign key.

.. code-block:: python

  from skibidi_orm.query_engine.field.field import CharField, IntegerField, ForeignKey
  from skibidi_orm.query_engine.model.base import Model
  from typing import Optional

  class Owner(Model):
    id: Optional[int | IntegerField] = IntegerField(primary_key=True)
    name: Optional[str | CharField] = CharField()

  class Dog(Model):
    id: Optional[int | IntegerField] = IntegerField(primary_key=True)
    name: Optional[str | CharField] = CharField('Reksio')
    owner: Optional[Owner | ForeignKey] = ForeignKey(to=Owner)

  bolek = Owner(1, "Bolek")
  lolek = Owner(2, "Lolek")
  reksio = Dog(1, "Reksio", bolek)
  lessie = Dog(2, "Lessie", owner_id=2)

You can give foreign key by object or by object id.
And you can use foreign key by itself.
*Podmienić kod*
.. code-block:: python

  from skibidi_orm.query_engine.field.field import CharField, IntegerField, ForeignKey
  from skibidi_orm.query_engine.model.base import Model
  from typing import Optional

  class Owner(Model):
    id: Optional[int | IntegerField] = IntegerField(primary_key=True)
    name: Optional[str | CharField] = CharField()

  class Dog(Model):
    id: Optional[int | IntegerField] = IntegerField(primary_key=True)
    name: Optional[str | CharField] = CharField('Reksio')
    owner: Optional[Owner | ForeignKey] = ForeignKey(to=Owner)

  bolek = Owner(1, "Bolek")
  lolek = Owner(2, "Lolek")
  reksio = Dog(1, "Reksio", bolek)
  lessie = Dog(2, "Lessie", owner_id=2)


Fields
==========

To możesz coś dać o atrybutach i rodzajach fieldów

