from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    ColumnSpecificConstraint,
    ForeignKeyConstraint,
)


@dataclass(unsafe_hash=True)
class BaseColumn[TDataTypes]:
    """
    Base column class that has to be properly implemented by the database specific column class.
    """

    name: str
    data_type: TDataTypes
    column_constraints: list[ColumnSpecificConstraint] = field(
        default_factory=list, hash=False
    )


@dataclass
class BaseTable[TCol]:
    """
    Base table class that has to be properly implemented by the database specific table class.
    """

    name: str
    columns: list[TCol] = field(default_factory=list)
    foreign_keys: set[ForeignKeyConstraint] = field(default_factory=set)


class BaseAdapter(ABC):
    """
    Base adapter class that has to be properly implemented by the database specific adapter class.
    """

    @abstractmethod
    def create_table(self, table: BaseTable[BaseColumn[Any]]):
        """Create a table in the database"""
        pass

    @abstractmethod
    def execute_migration(self, preview: bool = False):
        """Execute the migration"""
        pass
