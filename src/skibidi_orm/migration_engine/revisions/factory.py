from typing import Any

from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable
from skibidi_orm.migration_engine.revisions.revision import Revision
from skibidi_orm.migration_engine.revisions.snapshot import SchemaSnapshot


class RevisionFactory:
    """Class responsible for creating revision objects
    when migrating"""

    def create_revision_from_snapshot(self, snapshot: SchemaSnapshot) -> Revision:
        """Creates a revision based on a snpashot of the schema"""
        raise NotImplementedError()

    def create_schema_string(self, tables: list[BaseTable[Any]]) -> str:
        """Creates a human-readable schema representation based on
        all of the tables within it"""
        raise NotImplementedError()
