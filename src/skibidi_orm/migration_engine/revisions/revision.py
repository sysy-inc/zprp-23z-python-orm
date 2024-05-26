from dataclasses import dataclass, field


@dataclass
class Revision:
    """Class representing a single revision in the database.

    Attributes:
        id (int | Null): Unique id. Nulled before being saved into the database, which
        assigns the value using an autoincrementing id.

        timestamp (str): Timestamp of the creation.

        description (str): Migration message provided by the user when migrating.

        schema_repr (str): String representation of the schema.

        provider (str): Database provider.

        table_data (str): Serialized object containing information about tables, columns
        and constraints in the schema, based on which the schema can be recreated.
    """

    timestamp: str
    description: str
    schema_repr: str
    provider: str
    schema_data: bytes
    id: int | None = field(default_factory=lambda: None)

    def __str__(self) -> str:
        raise NotImplementedError()
