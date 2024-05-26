from typing import Any

from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable
from skibidi_orm.migration_engine.revisions.revision import Revision
from skibidi_orm.migration_engine.revisions.serialization import (
    serialize_tables,
)
from skibidi_orm.migration_engine.revisions.snapshot import SchemaSnapshot


class RevisionFactory:
    """Class responsible for creating revision objects
    when migrating"""

    @staticmethod
    def create_revision_from_snapshot(snapshot: SchemaSnapshot) -> Revision:
        """Creates a revision based on a snpashot of the schema by serializing
        its python objects into strings and bytes"""

        timestamp_str = snapshot.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        schema_data = serialize_tables(snapshot.tables)
        return Revision(
            timestamp=timestamp_str,
            description=snapshot.description,
            schema_repr=snapshot.schema_repr,
            provider=snapshot.provider,
            schema_data=schema_data,
        )

    def create_schema_string(self, tables: list[BaseTable[Any]]) -> str:
        """Creates a human-readable schema representation based on
        all of the tables within it"""
        raise NotImplementedError()
