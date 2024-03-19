from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Literal

type DataTypes = Literal[""]
type Constraints = Literal[""]


class BaseAdapter(ABC):
    type DataTypes = Literal[""]
    type Constraints = Literal[""]

    @dataclass
    class Column:
        name: str
        data_type: DataTypes
        constraints: list[Constraints] = field(default_factory=list)

    @dataclass
    class Table:
        name: str
        columns: list[BaseAdapter.Column] = field(default_factory=list)

    tables: list[Table] = []

    @abstractmethod
    def create_table(self, table_name: str, columns):
        """Create a table in the database"""
        pass

    @abstractmethod
    def execute_migration(self):
        """Execute the migration"""
        pass
