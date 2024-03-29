from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class BaseColumn[TDataTypes, TConstraints]:
    name: str
    data_type: TDataTypes
    constraints: list[TConstraints] = field(default_factory=list)


@dataclass
class BaseTable[TCol]:
    name: str
    columns: list[TCol] = field(default_factory=list)


class BaseAdapter(ABC):

    @abstractmethod
    def create_table(self, table: BaseTable[BaseColumn[Any, Any]]):
        """Create a table in the database"""
        pass

    @abstractmethod
    def create_relation(
        self,
        origin_table: str,
        origin_column: str,
        referenced_table: str,
        referenced_column: str,
    ):
        """Create a relation in the database"""
        pass

    @abstractmethod
    def execute_migration(self):
        """Execute the migration"""
        pass
