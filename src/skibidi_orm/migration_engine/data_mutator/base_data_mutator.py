from abc import ABC, abstractmethod

from pydantic import BaseModel, Field


class InsertRowColumn(BaseModel):
    name: str = Field(..., title="Column name")
    value: str = Field(..., title="Column value")


class BaseDataMutator(ABC):

    @abstractmethod
    def insert_row(self, table_name: str, row: list[InsertRowColumn]):
        pass
