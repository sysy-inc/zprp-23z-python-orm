"""
Module provides Session class, that handels executing orm operations like inserting to database,
selecting from database, etc.
"""

from skibidi_orm.query_engine.connection.engine import Engine
from skibidi_orm.query_engine.connection.identity import IdentityMap
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.connection.transaction import Transaction
from skibidi_orm.query_engine.operations.select import Select
from skibidi_orm.query_engine.connection.result import Result
from typing import Any, Optional, Type
from types import TracebackType


class Session:
    """
    Session is context manager and executes CRUD operations or selects
    on objects of our models

    Attributes:
        _engine (Engine): An object of class Engine that opens and stores connection to the database.
        _connection (Connection|None): Stores opened connection to the database.
        _new (list[Model]): A list of model instances to be inserted into the database.
        _dirty (list[Model]): A list of model instances with pending updates in the database.
        _delete (list[Model]): A list of model instances to be deleted from the database.
        _map (IdentityMap): An instance of IdentityMap to keep track of model instances and prevent duplicates.
    """
    def __init__(self, engine: Engine):
        """
        Initializes a Session and binds it with a given engine.

        Args:
            engine (Engine): An object of class Engine that distributes connection to the database.
        """
        self._engine = engine
        self._connection: Any = None
        self._new: list[Model] = []
        self._dirty: list[Model] = []
        self._delete: list[Model] = []
        self._map: IdentityMap = IdentityMap()

    def __enter__(self):
        """
        Takes a database connection from the engine when entering a 'with' block.
        """
        self._connection = self._engine.connect()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]):
        """
        Releases the database connection when exiting a 'with' block.
        Rolls back any uncommitted changes.

        Args:
            exc_type (Optional[Type[BaseException]]): The type of the exception (if any) that caused the exit.
            exc_value (Optional[BaseException]): The exception instance (if any) that caused the exit.
            traceback (Optional[TracebackType]): The traceback object (if any) that caused the exit.
        """
        self.close()

    def commit(self):
        """
        Commits any changes made to the database.

        Execute any pending operations that were stored in the given session (lazy execution).
        """
        self.flush()
        self._connection.commit()

    def rollback(self):
        """
        Rolls back changes in current transaction in database
        """
        self._connection.rollback()

    def close(self):
        """
        Ends session. Releases database connection to engine.
        Rolls back any uncommited changes, user needs to commit
        changes before closing session or they will be lost.
        """
        if self._connection:
            self.rollback()
            self._connection = None

    @property
    def connection(self):
        """
        Return stored connection to database
        """
        return self._connection

    def add(self, obj: Model):
        """
        Adds a model instance to the session and database.
        INSERT isn't executed right away (lazy execution concept)

        Args:
            obj (Model): The model instance to add.
        """
        if obj in self._map:
            # already added
            return
        obj._add_session(self)  # type: ignore
        self._new.append(obj)

    def _check_clear(self) -> bool:
        """
        Checks if there are any pending changes in the session.

        Returns:
            bool: True if there are no pending changes, False otherwise.
        """
        if self._new or self._delete or self._dirty:
            # not clear
            return False
        else:
            return True

    def changed(self, obj: Model):
        """
        Marks a model instance as changed in the session.
        UPDATE isn't executed right away (lazy execution concept)

        Args:
            obj (Model): The model instance that has changed.
        """
        o = self._map.get(obj._get_name_and_pk(), obj)  # type: ignore
        if o in self._dirty or o is None or o in self._delete:
            return
        if o not in self._map and o not in self._new:
            # object hasn't been added to this session
            return
        self._dirty.append(o)

    def delete(self, obj: Model):
        """
        Deletes a model instance from the session and database.
        DELETE isn't executed right away (lazy execution concept)

        Args:
            obj (Model): The model instance to delete.

        Raises:
            ValueError: if given object isn't part of a session (hasn't been added)
        """
        if obj in self._new:
            # object wasn't yet inserted so only delete from list to be inserted
            self._new.remove(obj)
            if obj in self._dirty:
                # remove from changed list
                self._dirty.remove(obj)
            return

        o = self._map.get(obj._get_name_and_pk(), None)     # type: ignore
        if o is None:
            raise ValueError("Given object is not part of session")
        else:
            if o in self._dirty:
                # if pending update, delete it, no need to update if it is deleted
                self._dirty.remove(o)
            o._remove_session()     # type: ignore
            self._delete.append(o)

    def flush(self):
        """
        Flushes any pending changes in the session to the database.
        """
        if not self._check_clear():
            # there are some pending changes
            config = self._engine.config
            trans = Transaction(config.compiler, self._connection)
            # INSERT
            for o in self._new:
                # TODO adjust for relations, order matters
                trans.register_insert(o)
                self._map.add(o)

            # UPDATE
            for o in self._dirty:
                trans.register_update(o)

            # DELETE
            for o in self._delete:
                trans.register_delete(o)

            trans.execute()
            self._new = []
            self._dirty = []
            self._delete = []

    def select(self, statement: Select):
        """
        Executes a select query and returns the results.
        Before execution flushes any pending changes to database.

        Args:
            statement (Select): The select query statement.

        Returns:
            list[Model | Result]: A list of model instances or result objects retrieved from the database.
        """
        self.flush()    # flush all pending changes
        comp = self._engine.config.compiler
        sql = comp.select(statement)
        cur = self._connection.cursor()
        cur.execute(sql)
        ret = cur.fetchall()

        result: list[Model | Result] = []
        column_names: list[str] = [description[0] for description in cur.description]
        rows: list[dict[str, Any]] = []
        for row in ret:
            row_dict: dict[str, Any] = dict(zip(column_names, row))
            rows.append(row_dict)

        if statement.returning_model:
            # select returns model
            for row in rows:
                model_class = statement.model
                obj = model_class(**row)
                obj_map = self._map.get(obj._get_name_and_pk(), None)      # type: ignore
                if obj_map is not None:
                    # if object in identity map return one from map to avoid duplicates
                    result.append(obj_map)
                else:
                    self._map.add(obj)  # add object to identity map
                    result.append(obj)
        else:
            # return named tuple
            for row in rows:
                result.append(Result(row))
        return result

    def get(self, model: Type[Model], primary_key: Any):
        """
        Retrieves a model instance from the database based on the provided primary key.

        Args:
            model (Type[Model]): The model class representing the type of object to retrieve.
            primary_key (Any): The primary key value of the object to retrieve.

        Returns:
            Model: The retrieved model instance from the database.
        """
        primary_key_name = model._get_primary_key_column()      # type: ignore
        st = Select(model).filter(**{primary_key_name: primary_key})
        ret = self.select(st)
        return ret[0]
