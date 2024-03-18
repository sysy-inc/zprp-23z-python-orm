from abc import ABC, abstractmethod
from typing import Literal, TypedDict


class BaseAdapter(ABC):
    type DataTypes = Literal[""]
    type Constraints = Literal[""]
    Column = TypedDict(
        "Column", {"name": str, "data_type": DataTypes, "constraints": Constraints}
    )

    @abstractmethod
    def create_table(self, table_name: str, columns):
        """Create a table in the database"""
        pass
