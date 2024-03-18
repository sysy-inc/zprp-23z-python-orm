from abc import ABC, abstractmethod
from typing import Literal


class BaseAdapter(ABC):
    type data_types = Literal[""]
    type constraints = Literal[""]

    @abstractmethod
    def create_table(self, table_name: str, columns):
        """Create a table in the database"""
        pass
