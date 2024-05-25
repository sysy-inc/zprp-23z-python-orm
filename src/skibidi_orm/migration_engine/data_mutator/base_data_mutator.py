from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel, Field


class InsertRowColumn(BaseModel):
    name: str = Field(..., title="Column name")
    value: str = Field(..., title="Column value")


class DeleteRowPk(BaseModel):
    name: str = Field(..., title="Primary key column name")
    value: str = Field(..., title="Primary key column value")


class BaseDataMutator(ABC):

    @abstractmethod
    def insert_row(self, table_name: str, row: list[InsertRowColumn]):
        """Insert a row in the table."""
        pass

    @abstractmethod
    def delete_row(self, table_name: str, pks: list[DeleteRowPk]):
        """Delete a row in the table. Row identified by primary key subset."""
        pass

    @abstractmethod
    def raw_query(self, query: str) -> list[Any]:
        """Execute a raw sql query in the database."""
        pass

    @abstractmethod
    def get_rows(self, table_name: str, limit: int = 100, offset: int = 0) -> list[Any]:
        """Get paginated rows from the table."""
        pass
