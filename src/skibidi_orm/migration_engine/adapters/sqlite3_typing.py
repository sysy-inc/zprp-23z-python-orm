from typing import Literal
from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseColumn,
    Relation,
    BaseTable,
)

from skibidi_orm.migration_engine.operations.constraints import Constraint


class SQLite3Typing:

    DataTypes = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
    Constraints = Constraint
    Column = BaseColumn[DataTypes]
    Table = BaseTable[Column]
    Relation = Relation
    tables: list[Table] = []
    relations: list[Relation] = []
