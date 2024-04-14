from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from skibidi_orm.migration_engine.operations.constraints import Constraint


@dataclass(unsafe_hash=True)
class BaseColumn[TDataTypes]:
    name: str
    data_type: TDataTypes
    constraints: list[Constraint] = field(default_factory=list, hash=False)


@dataclass
class BaseTable[TCol]:
    name: str
    columns: list[TCol] = field(default_factory=list)


@dataclass
class Relation:
    origin_table: str
    origin_column: str
    referenced_table: str
    referenced_column: str


class BaseAdapter(ABC):

    @abstractmethod
    def create_table(self, table: BaseTable[BaseColumn[Any]]):
        """Create a table in the database"""
        pass

    @abstractmethod
    def create_relation(self, relation: Relation):
        """Create a relation in the database"""
        pass

    @abstractmethod
    def execute_migration(self):
        """Execute the migration"""
        pass
