"""
Module handels executing orm operations like inserting to database, selecting from data
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
    Session is context manager and executes CRUD operations
    on objects of our models

    Attributes:
    _engine(Engine): object of class Engine that opens and stores connection to database
    _connection(Connection|None): stores opened connection to database
    """
    def __init__(self, engine: Engine):
        """
        Initializes Session and binds it with given engine.

        :param engine(Engine): object of class Engine that distributes
                               connection to database
        """
        self._engine = engine
        self._connection: Any = None
        self._new: list[Model] = []
        self._dirty: list[Model] = []
        self._delete: list[Model] = []
        self._map: IdentityMap = IdentityMap()

    def __enter__(self):
        """
        Takes database connection from engine when entering a 'with' block.
        """
        self._connection = self._engine.connect()
        return self

    def __exit__(self, exc_type: Optional[Type[BaseException]],
                 exc_value: Optional[BaseException],
                 traceback: Optional[TracebackType]):
        """
        Releases database connection when exiting a 'with' block.
        Rolls back any uncommited changes

        :param exc_type: The type of the exception (if any) that caused the exit.
        :param exc_value: The exception instance (if any) that caused the exit.
        :param traceback: The traceback object (if any) that caused the exit.
        """
        self.close()

    def commit(self):
        """
        Commit any changes made to database

        In future it will also execute any pending operations
        that where stored in given session (lazy execution)
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

        In future it will also remove any pending operations
        that where stored in given session (lazy execution)
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
        if obj in self._map:
            # already added
            return
        # TODO register this session to model, model.add_session()
        self._new.append(obj)

    def _check_clear(self) -> bool:
        if self._new or self._delete or self._dirty:
            # not clear
            return False
        else:
            return True

    def changed(self, obj: Model):
        # o = self._map.get(obj.key(), obj) TOCHANGE
        o = self._map.get(("test_model", 1), obj)
        if o in self._dirty or o is None or o in self._delete:
            return
        if o not in self._map and o not in self._new:
            # object hasn't been add to this session
            return
        self._dirty.append(o)

    def delete(self, obj: Model):
        # o = self._map.get(obj.key(), None) TOCHANGE
        if obj in self._new:
            # object wasn't yet inserted so only delete from list to be inserted
            self._new.remove(obj)
            if obj in self._dirty:
                self._dirty.remove(obj)
            return

        o = self._map.get(("test_model", 1), None)
        if o is None:
            raise ValueError("Given object is not part of session")
        else:
            if o in self._dirty:
                # if pending update, delete it, no need to update if it is deleted
                self._dirty.remove(o)
            # TODO tell model to remove session from attributes
            self._delete.append(o)

    def flush(self):
        if not self._check_clear():
            # there are some pending changes
            config = self._engine.config
            trans = Transaction(config.compiler, self._connection)
            # INSERT
            for o in self._new:
                # TODO adjust for relations, order matters
                trans.register_insert(o)
                self._map.add(o)
            # for o in self._new:
            #     # TODO maybe add function register_pending that adds to map and cleans _new
            #     self._map.add(o)

            # UPDATE
            for o in self._dirty:
                # TODO check if in delete, no need to update if
                trans.register_update(o)

            # DELETE
            for o in self._delete:
                trans.register_delete(o)

            trans.execute()
            self._new = []
            self._dirty = []
            self._delete = []

    def select(self, statement: Select):
        self.flush()    # flush all pending changes
        comp = self._engine.config.compiler
        sql = comp.select(statement)
        cur = self._connection.cursor()
        cur.execute(sql)
        ret = cur.fetchall()

        result: list[Model | Result] = []     # TODO make class for this
        column_names: list[str] = [description[0] for description in cur.description]
        rows: list[dict[str, Any]] = []
        for row in ret:
            row_dict: dict[str, Any] = dict(zip(column_names, row))
            rows.append(row_dict)

        if statement.returning_model:
            # select returns model
            for row in rows:
                model_class = statement.model
                print(row)
                result.append(model_class(**row))
                # TODO add to identity map
        else:
            # return named tuple
            for row in rows:
                result.append(Result(row))
        return result

    def get(self, model: Type[Model], primary_key: Any):
        primary_key_name = "id"     # TOCHANGE function from Model
        st = Select(model).filter(**{primary_key_name: primary_key})
        ret = self.select(st)
        return ret[0]
