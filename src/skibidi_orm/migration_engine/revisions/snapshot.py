from datetime import datetime
from dataclasses import dataclass, field
from typing import Any

from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable
from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig


@dataclass
class SchemaSnapshot:
    """Class representing a snapshot of the schema at a given time.
    After serializing the snapshot, it is stored in the revision table.
    It serves as a way to hold data about the database schema before it's
    serialized, using python objects instead of database friendly datatypes.

    Attributes:
        timestamp (datetime): Timestamp of the creation.

        description (str): Migration message provided by the user when migrating.

        schema_repr (str): String representation of the schema.

        config (BaseDbConfig): Serialized BaseDbConfig deriving object used when migrating.

        tables (list[BaseTable]): List of tables in the schema.
    """

    timestamp: datetime = field(init=False, default_factory=lambda: datetime.now())
    description: str
    schema_repr: str
    config: BaseDbConfig
    tables: list[BaseTable[Any]]
