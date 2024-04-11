"""
Module handels executing orm operations like inserting to database, selecting from data
"""

from skibidi_orm.query_engine.connection.engine import Engine
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
