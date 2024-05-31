from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    ColumnWideConstraint,
    TableWideConstraint,
)


@dataclass(unsafe_hash=True)
class BaseColumn[TDataTypes]:
    """
    Base column class that has to be properly implemented by the database specific column class.
    """

    name: str
    data_type: TDataTypes
    column_constraints: list[ColumnWideConstraint] = field(
        default_factory=list, hash=False
    )


@dataclass
class BaseTable[TCol]:
    """
    Base table class that has to be properly implemented by the database specific table class.
    """

    name: str
    columns: list[TCol] = field(default_factory=list)
    table_constraints: list[TableWideConstraint] = field(default_factory=list)


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
