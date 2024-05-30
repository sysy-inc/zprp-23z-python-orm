from typing import Literal
from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseColumn,
    BaseTable,
)

from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    Constraint,
)


class PostgresTyping:

    DataTypes = Literal[
        "BIGINT",
        "BIGSERIAL",
        "BIT",
        "BIT VARYING",
        "BOOLEAN",
        "BOX",
        "BYTEA",
        "CHARACTER",
        "CHARACTER VARYING",
        "CIDR",
        "CIRCLE",
        "DATE",
        "DOUBLE PRECISION",
        "INET",
        "INTEGER",
        "INTERVAL",
        "JSON",
        "JSONB",
        "LINE",
        "LSEG",
        "MACADDR",
        "MACADDR8",
        "MONEY",
        "NUMERIC",
        "PATH",
        "PG_LSN",
        "POINT",
        "POLYGON",
        "REAL",
        "SMALLINT",
        "SMALLSERIAL",
        "SERIAL",
        "TEXT",
        "TIME",
        "TIME WITH TIME ZONE",
        "TIMESTAMP",
        "TIMESTAMP WITH TIME ZONE",
        "TIMESTAMP WITHOUT TIME ZONE",
        "TSQUERY",
        "TSVECTOR",
        "TXID_SNAPSHOT",
        "UUID",
        "XML",
    ]
    Constraints = Constraint
    Column = BaseColumn[DataTypes]
    Table = BaseTable[Column]
