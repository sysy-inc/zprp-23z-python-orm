"""
Module handles configuration data (needed to open connection) for different databases
"""
from abc import ABC, abstractmethod
from typing import Any
from skibidi_orm.query_engine.adapter.sqlite_adapter import SQLiteAdapter


class Config(ABC):
    """
    Abstract base class for configuration
    Stores all of data needed to connect to database

    Subclasses must implement the __init__()
    """
    @abstractmethod
    def __init__(self, **kwargs: dict[str, Any]) -> None:
        self._adapter = None

    @property
    def adapter(self):
        """
        Return correct adapter for this database
        """
        return self._adapter


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
