"""
Module handles connections to database: open connection, store it and close
"""

from skibidi_orm.query_engine.config import Config
from typing import Any


class Engine:
    """
    Engine manages connection, stores it and closes at the end

    Attributes:
    _config(Config): object of class Config or its subclasses, representing
                     configuration of database
    _connection(Connection|None): stores opened connection to database
    _is_connected(bool): determines whether there is already open connection(True)
                         or connection hasn't been opened yet(False)
    _adapter(Adapter): adapter for database given in config
    """
    def __init__(self, config: Config) -> None:
        """
        Initializes Engine with the given configuration.

        :param config(Config): object of class Config or its subclasses, representing
                               configuration of database.
        """
        self._config = config
        self._connection: Any = None
        self._is_connected: bool = False
        self._adapter = config.adapter

    def connect(self) -> object:
        """
        Opens connection to database if it hasn't been opened yet.
        Returns opened connection to database(Connection)
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
        Closes connection to database if one is opened
        """
        if self._connection:
            self._connection.close()
            self._is_connected = False

    def __del__(self):
        """
        Upon deletion of this object close connection if it is still open
        """
        self.close()

    @property
    def connected(self) -> bool:
        """
        Return whether there is open connection or not
        """
        return self._is_connected
