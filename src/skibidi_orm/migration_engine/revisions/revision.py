from datetime import datetime
from dataclasses import dataclass, field
from typing import Any
import sqlite3
import pickle

from skibidi_orm.migration_engine.adapters.base_adapter import BaseColumn, BaseTable
from skibidi_orm.migration_engine.adapters.providers import DatabaseProvider


@dataclass
class Revision:
    """Class representing a revision of the schema at a given time.
    After serializing it, it is stored in the revision table.
    Every database provider has to take care of adapting and converting it
    before inserting it into the table.

    Attributes:
        timestamp (datetime): Timestamp of the creation.

        description (str): Migration message provided by the user when migrating.

        schema_repr (str): String representation of the schema.

        provider (str): Database provider.

        tables (list[BaseTable]): List of tables in the schema.
    """

    timestamp: datetime = field(init=False, default_factory=lambda: datetime.now())
    description: str
    schema_repr: str
    provider: DatabaseProvider
    tables: list[BaseTable[BaseColumn[Any]]]

    def __conform__(self, protocol: Any):
        """This method is used to serialize the object before inserting it into the database.
        Every database provider has to take care of adapting and converting it."""
        if protocol is sqlite3.PrepareProtocol:
            return pickle.dumps(self)

    @staticmethod
    def deserialize(data: bytes):
        """Deserializes the data from the database."""
        return pickle.loads(data)


# register the converter function which deserializes the object
sqlite3.register_converter("REVISION", Revision.deserialize)
