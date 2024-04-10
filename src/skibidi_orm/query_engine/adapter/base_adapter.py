"""
Base class for adapter. Used for managing making connection
by different databases
"""
from abc import ABC, abstractmethod
from typing import Any


class Adapter(ABC):
    """
    Abstract base class for database adapters.

    Subclasses must implement the _import_connector() method to import
    the appropriate database connector, and the make_connection() method
    to create a connection with the given parameters.
    """
    def __init__(self) -> None:
        self._connector = None

    @abstractmethod
    def _import_connector(self):
        """
        Imports connector for specific database
        """
        pass

    @abstractmethod
    def make_connection(self, **kwargs: dict[str, Any]):
        """
        Creates connection with given parameters and returns it
        :param kwargs: keyword arguments for configuring the database connection
        """
        pass
