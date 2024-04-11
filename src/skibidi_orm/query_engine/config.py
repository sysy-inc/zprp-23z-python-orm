"""
Module handles configuration data (needed to open connection) for different databases
"""
from abc import ABC, abstractmethod
from typing import Any
from skibidi_orm.query_engine.adapter.sqlite_adapter import SQLiteAdapter
from skibidi_orm.query_engine.adapter.base_adapter import Adapter


class Config(ABC):
    """
    Abstract base class for configuration
    Stores all of data needed to connect to database

    Subclasses must implement the __init__()
    """
    @abstractmethod
    def __init__(self, **kwargs: dict[str, Any]) -> None:
        self._adapter: Adapter = NotImplemented

    @property
    def adapter(self) -> Adapter:
        """
        Return correct adapter for this database
        """
        return self._adapter

    @abstractmethod
    def connection_data(self) -> dict[str, Any]:
        """
        Prepare and return data needed for opening connection
        """
        pass


class SQLiteConfig(Config):
    """
    Configuration class for database sqlite
    """
    def __init__(self, **kwargs: dict[str, Any]) -> None:
        """
        Create instance of SQLiteConfig
        :param kwargs: keyword arguments to specify database configuration
            - path(str): path to sqlite database

        Example
        SQLiteConfig(path='database.db)
        """
        super().__init__(**kwargs)
        self._database_path = kwargs.get('path', '')
        self._adapter = SQLiteAdapter()

    def connection_data(self):
        return {'path': self._database_path}
