from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Revision:
    """Class representing a single revision in the database.

    Attributes:
        id (int): Unique id.

        timestamp (datetime): Timestamp of the migration.

        description (str): Migration message provided by the user when migrating.

        schema_repr (str): String representation of the schema.

        config_data (str): Serialized BaseDbConfig deriving object used when migrating.

        table_data (str): Serialized object containing information about tables, columns
        and constraints in the schema, based on which the schema can be recreated.
    """

    id: int
    timestamp: datetime
    description: str
    schema_repr: str
    config_data: bytes
    table_data: bytes

    def __str__(self) -> str:
        raise NotImplementedError()
