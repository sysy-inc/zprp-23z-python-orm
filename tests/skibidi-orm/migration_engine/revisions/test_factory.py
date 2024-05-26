from typing import Any
from skibidi_orm.migration_engine.adapters.base_adapter import BaseColumn, BaseTable
from skibidi_orm.migration_engine.revisions.factory import RevisionFactory
from skibidi_orm.migration_engine.revisions.serialization import (
    serialize_tables,
)
from skibidi_orm.migration_engine.revisions.snapshot import SchemaSnapshot
from freezegun import freeze_time


@freeze_time("2023-12-31 23:59:59")
def test_revision_from_snapshot():
    """Test the correctness of the revision created from a snapshot."""
    snapshot = SchemaSnapshot(
        description="Test description",
        schema_repr="Test schema representation",
        provider="Test provider",
        tables=[BaseTable[BaseColumn[Any]]("test", [])],
    )
    revision = RevisionFactory.create_revision_from_snapshot(snapshot)
    assert revision.timestamp == "2023-12-31 23:59:59"
    assert revision.description == "Test description"
    assert revision.schema_repr == "Test schema representation"
    assert revision.provider == "Test provider"
    assert revision.schema_data == serialize_tables(snapshot.tables)
