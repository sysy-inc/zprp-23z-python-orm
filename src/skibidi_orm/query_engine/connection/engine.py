"""
This module provides the Engine class, which is responsible for managing database connections.
The Engine class handles opening and closing connections to the database, ensuring that only
one connection is open at any time.
"""

from skibidi_orm.query_engine import config
from typing import Any


class Engine:
    """
    Manages database connections, including opening and closing them.

    Attributes:
        _config (Config): An object of class Config or its subclasses, representing
                          the configuration of the database.
        _connection (Connection|None): Stores the opened connection to the database.
        _is_connected (bool): Indicates whether a connection is already open (True)
                              or has not been opened yet (False).
        _adapter (Adapter): Adapter for the database specified in the configuration.
    """
    def __init__(self) -> None:
        """
        Initializes the Engine instance, setting up the configuration and adapter.
        """
        self._config = config.get_configuration()
        self._connection: Any = None
        self._is_connected: bool = False
        self._adapter = self._config.adapter

    def connect(self) -> object:
        """
        Opens a connection to the database if it hasn't been opened yet.

        Returns:
            Connection: The opened connection to the database.
        """
        if not self._is_connected:
            # connection hasn't been opened yet
            data = self._config.connection_data()   # get data needed for connection
            connection = self._adapter.make_connection(**data)
            self._connection = connection
            self._is_connected = True
        return self._connection

    def close(self) -> None:
        """
        Closes the connection to the database if one is open.
        """
        if self._connection:
            self._connection.close()
            self._is_connected = False

    def __del__(self):
        """
        Ensures the connection is closed upon deletion of this object.
        """
        self.close()

    @property
    def connected(self) -> bool:
        """
        Indicates whether a connection is currently open.

        Returns:
            bool: True if a connection is open, False otherwise.
        """
        return self._is_connected

    @property
    def config(self):
        """
        Returns the configuration of the database.

        Returns:
            Config: The configuration object.
        """
        return self._config
