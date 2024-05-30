"""
Module handles configuration data (needed to open connection) for different databases
"""
from abc import ABC, abstractmethod
from typing import Any
from skibidi_orm.query_engine.adapter.sqlite_adapter import SQLiteAdapter
from skibidi_orm.query_engine.adapter.base_adapter import Adapter
from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler


class Config(ABC):
    """
    Abstract base class for configuration.

    Stores all data needed to connect to a database.

    Subclasses must implement the __init__() method.
    """
    @abstractmethod
    def __init__(self, **kwargs: Any) -> None:
        """
        Initializes the configuration object.

        Args:
            **kwargs (Any): Keyword arguments to configure the database.

        Raises:
            NotImplementedError: If the method is not implemented in the subclass.
        """
        self._adapter: Adapter = NotImplemented

    @property
    def adapter(self) -> Adapter:
        """
        Returns the correct adapter for this database.

        Returns:
            Adapter: The adapter object.
        """
        return self._adapter

    @property
    def compiler(self) -> SQLCompiler:
        """
        Returns the SQL compiler associated with the adapter.

        Returns:
            SQLCompiler: The SQL compiler object.
        """
        return self._adapter.compiler

    @abstractmethod
    def connection_data(self) -> dict[str, Any]:
        """
        Prepares and returns the data needed for opening a connection.

        Returns:
            dict[str, Any]: A dictionary containing connection data.
        """
        pass


class SQLiteConfig(Config):
    """
    Configuration class for SQLite database.
    """
    def __init__(self, **kwargs: str) -> None:
        """
        Initializes an instance of SQLiteConfig.

        Args:
            **kwargs (str): Keyword arguments to specify database configuration.
                - path (str): Path to the SQLite database file.

        Example:
            SQLiteConfig(path='database.db')
        """
        super().__init__(**kwargs)
        self._database_path = kwargs.get('path', '')
        self._adapter = SQLiteAdapter()

    def connection_data(self):
        """
        Prepares and returns data needed for opening a connection.

        Returns:
            dict[str, Any]: A dictionary containing the path to the SQLite database.
        """
        return {'path': self._database_path}


def get_configuration() -> Config:
    """
    Retrieves the configuration object from the configuration file.

    Checks if a configuration file exists in the working directory and reads
    configuration data from it.

    Expected configuration file: configuration.py
    The file should contain a variable named 'config_data' which stores an object
    of a subclass of Config representing the chosen database configuration.

    Returns:
        Config: The configuration object.

    Raises:
        Exception: If there is no configuration file found.
    """
    try:
        from configuration import config_data  # type: ignore
        return config_data  # type: ignore

    except ImportError:
        raise Exception("There is no configuration.py file. Please create one")
