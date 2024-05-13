from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any
from skibidi_orm.migration_engine.operations.constraints import (
    ColumnSpecificConstraint,
    ForeignKeyConstraint,
)


@dataclass
class BaseColumn[TDataTypes]:
    name: str
    data_type: TDataTypes
    column_constraints: list[ColumnSpecificConstraint] = field(default_factory=list)


@dataclass
class BaseTable[TCol]:
    name: str
    columns: list[TCol] = field(default_factory=list)
    foreign_keys: set[ForeignKeyConstraint] = field(default_factory=set)


class BaseAdapter(ABC):

    @abstractmethod
    def create_table(self, table: BaseTable[BaseColumn[Any]]):
        """Create a table in the database"""
        pass

    @abstractmethod
    def execute_migration(self):
        """Execute the migration"""
        pass
