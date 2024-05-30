"""
Base class for adapter. Used for managing making connection
by different databases
"""
from abc import ABC, abstractmethod
from typing import Any
from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler


class Adapter(ABC):
    """
    Abstract base class for database adapters.

    Subclasses must implement the `_import_connector()` method to import
    the appropriate database connector, and the `make_connection()` method
    to create a connection with the given parameters.
    """
    def __init__(self) -> None:
        """
        Initializes an Adapter instance.

        Initializes the connector to None and sets up the SQL compiler.
        """
        self._connector = None
        self._compiler = SQLCompiler()

    @abstractmethod
    def _import_connector(self):
        """
        Imports the connector for the specific database.
        """
        pass

    @abstractmethod
    def make_connection(self, **kwargs: Any) -> object:
        """
        Creates a connection with the given parameters and returns it.

        Args:
            **kwargs: Keyword arguments for configuring the database connection.

        Returns:
            object: A connection object for the specific database.
        """
        pass

    @property
    def connector(self):
        """
        The database connector.

        Returns:
            object: The connector to the database.
        """
        return self._connector

    @property
    def compiler(self):
        """
        The SQL compiler.

        Returns:
            SQLCompiler: The compiler used to compile SQL queries.
        """
        return self._compiler
