"""
Module handles configuration data (needed to open connection) for different databases
"""
from abc import ABC, abstractmethod
from typing import Any


class Config(ABC):
    """
    Abstract Base class for configuration
    Stores all of data needed to connect to database
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
