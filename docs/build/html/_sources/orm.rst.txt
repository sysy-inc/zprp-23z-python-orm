======================
ORM
======================

How to connect to database?
===============================

Now, when we created model, it is time to connect to the database.

Step 1: Create Configuration
------------------------------
In order to connect to database, you have to specify which database you want to use.
In your working directory create file  **configuration.py** and in it specify variable
*config_data* with data neede for chosen database.

Example for SQLite

configuration.py

.. code-block:: python

	from skibidi_orm.query_engine.config import SQLiteConfig

	config_data = SQLiteConfig(path="database.db")

Where *path* represents where your database file is stored.

Step 2: Create Engine
----------------------
Engine handles all connections to database, it opens connection and when all is done, closes it.

.. code-block:: python

    from skibidi_orm.query_engine.connection.engine import Engine

    eng = Engine()

Now when we have connection started, it is time to use it.

Step 3: Session
-----------------
All operations to database are made in session. At the end you **need to commit** all the changes or they won't be saved to database.

Basic usage of session

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session

  eng = Engine()	# create engine

  with Session(eng) as session:
    # perform all operations
    session.commit()	# commit changes

Add object to database
========================
When we have our model ready, it is time to save some objects into our database.
It can be done by *session.add()* method.

First lets create a basic model.

.. code-block:: python

  from skibidi_orm.query_engine.field.field import CharField, IntegerField
  from skibidi_orm.query_engine.model.base import Model
  from typing import Optional

  class Person(Model):
    id: Optional[int | IntegerField] = IntegerField(primary_key=True)
    name: Optional[str | CharField] = CharField(default='Adam')
    age: Optional[int | IntegerField] = IntegerField(default=30)

Now lets add it to our session.

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session

  eng = Engine()	# create engine

  with Session(eng) as session:
    person = Person(1, 'Adam', 20)	# create instance of model
    session.add(person)		# add it to session
    session.commit()	# commit changes

Change of value
================
If we change value of some object's attribute (inside session) it is automatically saved in database, you don't need to do anything.

Lets go back to previous example.

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session

  eng = Engine()	# create engine

  with Session(eng) as session:
    person = Person(1, 'Adam', 20)	# create instance of model
    session.add(person)		# add it to session
    person.age = 25		# change value
    session.commit()	# commit changes

Remove object from database
============================
Now we know how to add object to database and change its values, but what if we want to remove one. It can be done using *session.delete*.

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session

  eng = Engine()	# create engine

  with Session(eng) as session:
    person = Person(1, 'Adam', 20)	# create instance of model
    session.add(person)		# add it to session
    session.commit()	# commit changes
    # .....
    # remove previously added person
    session.delete(person)

We can delete object before commiting changes or after.

Get data from database
=======================
To retrieve data from database, we need to execute select. It is done by using class *Select*.

Lets assume that we saved to database *person = Person(1, 'Adam', 20)* from previous example. Now in new session we want retrieve this data.

Lets create basic select, like *SELECT id, name, age FROM person;*

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session
  from skibidi_orm.query_engine.operations.select import Select

  eng = Engine()	# create engine

  with Session(eng) as session:
    st = Select(Person)
    ret = session.select(st)
    for r in ret:
      print(f"Id: {r.id} Name: {r.name} Age: {r.age}")
      # output: Id: 1 Name: Adam Age 20

When retrieving data, our library makes sure that we don't have duplicates present in session.

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session
  from skibidi_orm.query_engine.operations.select import Select

  eng = Engine()	# create engine

  with Session(eng) as session:
    person = Person(1, 'Adam', 20)	# create instance of model
    session.add(person)		# add it to session
    session.commit()	# commit changes
    # .......

    st = Select(Person)
    ret = session.select(st)
    for r in ret:
      print(f"Id: {r.id} Name: {r.name} Age: {r.age}")
      # output: Id: 1 Name: Adam Age 20

    select_person = ret[0]
    print(select_person == person)	# output: True
    # if we change value in one, it is changed in another
    person.age = 25
    print(select_person.age)	# output: 25

Retrieve object by primary key
-------------------------------
If we want to retrieve object with given primary key, we use *session.get()*.

Lets say that in our database we have saved *person = Person(1, 'Adam', 20)* and we want to retrieve it by the primary key *1*.

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session

  eng = Engine()	# create engine

  with Session(eng) as session:
    ret = session.get(Person, 1)
    print(f"Id: {r.id} Name: {r.name} Age: {r.age}")
    # output: Id: 1 Name: Adam Age 20

Order by
----------
We can order our select's result by specific column. You can use ascending or descending order (by default it is set ascending). You need to specify by which column to order *.order_by("chosen_column")* and for descending order set desc to True *.order_by("chosen_column", desc=True)*.

Lets add to our database couple of objects

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session

  eng = Engine()	# create engine

  with Session(eng) as session:
    person1 = Person(1, 'Adam', 20)	# create instance of model
    person2 = Person(2, 'Kate', 18)
    person3 = Person(3, 'Thom', 30)
    session.add(person1)		# add it to session
    session.add(person2)
    session.add(person3)
    session.commit()	# commit changes

And now perform select with order by

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session
  from skibidi_orm.query_engine.operations.select import Select

  eng = Engine()	# create engine

  with Session(eng) as session:
    # order results by age
    st = Select(Person).order_by("age")
    ret = session.select(st)
    for r in ret:
      print(f"Id: {r.id} Name: {r.name} Age: {r.age}")
      # output: Id: 3 Name: Kate Age 18
      # output: Id: 1 Name: Adam Age 20
      # output: Id: 2 Name: Thom Age 30

    # order results by age with descending order
    st = Select(Person).order_by("age", desc=True)
    ret = session.select(st)
    for r in ret:
      print(f"Id: {r.id} Name: {r.name} Age: {r.age}")
      # output: Id: 2 Name: Thom Age 30
      # output: Id: 1 Name: Adam Age 20
      # output: Id: 3 Name: Kate Age 18

Group by
----------
We can group our select's result by specific column. You need to specify by which column to group by *.group_by("chosen_column")*.

Lets add some object to database

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session

  eng = Engine()	# create engine

  with Session(eng) as session:
    person1 = Person(1, 'Adam', 20)	# create instance of model
    person2 = Person(2, 'Kate', 20)
    person3 = Person(3, 'Thom', 30)
    person3 = Person(4, 'Ann', 40)
    session.add(person1)		# add it to session
    session.add(person2)
    session.add(person3)
    session.add(person4)
    session.commit()	# commit changes

We have one person with age 30, one with 40 and two with 20.

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session
  from skibidi_orm.query_engine.operations.select import Select

  eng = Engine()	# create engine

  with Session(eng) as session:
    # group results by age
    st = Select(Person).group_by("age")
    ret = session.select(st)
    for r in ret:
      print(f"Age: {r.age}")
      # output:Age 20
      # output:Age 30
      # output:Age 40

Aggregate function
--------------------
When we group by our result we can use function COUNT on other columns.

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session

  eng = Engine()	# create engine

  with Session(eng) as session:
    person1 = Person(1, 'Adam', 20)	# create instance of model
    person2 = Person(2, 'Kate', 20)
    person3 = Person(3, 'Thom', 30)
    person3 = Person(4, 'Ann', 40)
    session.add(person1)		# add it to session
    session.add(person2)
    session.add(person3)
    session.add(person4)
    session.commit()	# commit changes

We have one person with age 30, one with 40 and two with 20, we can count how many is there in each group by using count on column id.

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session
  from skibidi_orm.query_engine.operations.select import Select
  from skibidi_orm.query_engine.operations.functions import Count

  eng = Engine()	# create engine

  with Session(eng) as session:
    # group results by age
    st = Select(Person).group_by("age").annotate(count=Count("id"))
    ret = session.select(st)
    for r in ret:
      print(f"Age: {r.age} Count: {r.count}")
      # output: Age: 20 Count: 2
      # output: Age: 30 Count: 1
      # output: Age: 40 Count: 1

*.annotate()* is used to give name to resulting column.

Filter results
---------------
We can filter our results by different conditions. We use *.filter(column_name=3, another_name__gte=3)*. We create different conditions, like greather than, by adding **__** to column's name, followed by specific option we want to use.

Options that can by used:

* column_name=2 -> this is equality condition
* column_name__gt=2 -> greater than
* column_name__gte=2 -> greater than or equal
* column_name__lt=2 -> less than
* column_name__lte=2 -> less than or equal
* column_name__not=2 -> not equal, column_name != 2
* column_name__isnull=True -> is Null
* column_name__isnull=False -> is not Null

Example

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session

  eng = Engine()	# create engine

  with Session(eng) as session:
    person1 = Person(1, 'Adam', 20)	# create instance of model
    person2 = Person(2, 'Kate', 20)
    person3 = Person(3, 'Thom', 30)
    person4 = Person(4, 'John', 30)
    person5 = Person(5, 'Ann', 40)
    session.add(person1)		# add it to session
    session.add(person2)
    session.add(person3)
    session.add(person4)
    session.add(person5)
    session.commit()	# commit changes


.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session
  from skibidi_orm.query_engine.operations.select import Select

  eng = Engine()	# create engine

  with Session(eng) as session:
    # filter results age>20 and name='John'
    st = Select(Person).filter(age__gt=20, name='John')
    ret = session.select(st)
    for r in ret:
      print(f"Id: {r.id} Name: {r.name} Age: {r.age}")
      # output: Id: 4 Name: John Age: 30

Select multiple methods
------------------------
We can use together all this methods, like in real select statement in sql

.. code-block:: python

  from skibidi_orm.query_engine.connection.engine import Engine
  from skibidi_orm.query_engine.connection.session import Session
  from skibidi_orm.query_engine.operations.select import Select

  eng = Engine()	# create engine

  with Session(eng) as session:
    st = Select(Person).filter(age__gt=20).order_by("id", desc=True)
    ret = session.select(st)
