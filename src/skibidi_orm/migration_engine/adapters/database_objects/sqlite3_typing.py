from typing import Literal
from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseColumn,
    BaseTable,
)

from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    Constraint,
)


class SQLite3Typing:

    DataTypes = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
    Constraints = Constraint
    Column = BaseColumn[DataTypes]
    Table = BaseTable[Column]
    tables: list[Table] = []