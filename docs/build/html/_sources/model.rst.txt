======================
Model
======================

How to create your own model?
===============================

Welcome to skibidi project! With our library, you can create a database model!

Every model should inherit from the class 'Model'.

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


*__db_table__* is an optional attribute, representing the name of a table in your database. The rest of the attributes are mapped to the database columns. You can add new attributes using the following pattern: *'attr_name: Optional[python_type | FieldType] = FieldType()'*. You can define the primary key by yourself, using the *AutoField*, but skibidi can also do this for you automatically.

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

You can create your foreign key.

.. code-block:: python

  from skibidi_orm.query_engine.field.field import CharField, IntegerField
  from skibidi_orm.query_engine.field.related_field import ForeignKey
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

You can provide foreign key by object or by object id.
You can also create a recursive foreign key.

.. code-block:: python

  from skibidi_orm.query_engine.field.field import CharField, IntegerField
  from skibidi_orm.query_engine.field.related_field import ForeignKey
  from skibidi_orm.query_engine.model.base import Model
  from typing import Optional, ForwardRef

  DogType: Optional['Dog'] = ForwardRef('Dog')

  class Dog(Model):
    id: Optional[int | IntegerField] = IntegerField(primary_key=True)
    name: Optional[str | CharField] = CharField('Reksio')
    friend: Optional[DogType | ForeignKey] = ForeignKey(to='self')

  maks = Dog(1, 'Maks')
  reks = Dog(2, "Reks", maks)


Fields
==========

To możesz coś dać o atrybutach i rodzajach fieldów

