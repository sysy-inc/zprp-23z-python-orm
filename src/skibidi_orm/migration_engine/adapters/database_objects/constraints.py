from abc import ABC
import enum
from dataclasses import dataclass, field


class ConstraintType(enum.Enum):
    """All supported constraint types"""

    NOT_NULL = "NOT NULL"
    UNIQUE = "UNIQUE"
    PRIMARY_KEY = "PRIMARY KEY"
    FOREIGN_KEY = "FOREIGN KEY"
    CHECK = "CHECK"
    DEFAULT = "DEFAULT"


@dataclass(frozen=True)
class Constraint(ABC):
    """Base class for all constraints"""

    constraint_type: ConstraintType = field(init=False)
    table_name: str


@dataclass(frozen=True)
class ColumnWideConstraint(Constraint):
    """Base class for constraints that apply to a column instead of multiple (e.g. composite foreign keys)"""

    column_name: str


@dataclass(frozen=True)
class TableWideConstraint(Constraint):
    """Base class for constraints that apply to a table - foreign keys and check constraints"""


@dataclass(frozen=True)
class NotNullConstraint(ColumnWideConstraint):
    """Class for the NOT NULL constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.NOT_NULL)


@dataclass(frozen=True)
class UniqueConstraint(ColumnWideConstraint):
    """Class for the UNIQUE constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.UNIQUE)


@dataclass(frozen=True)
class PrimaryKeyConstraint(ColumnWideConstraint):
    """Class for the PRIMARY KEY constraint"""

    constraint_type: ConstraintType = field(
        init=False, default=ConstraintType.PRIMARY_KEY
    )


@dataclass(frozen=True, unsafe_hash=True)
class ForeignKeyConstraint(TableWideConstraint):
    """Class for the FOREIGN KEY constraint"""

    constraint_type: ConstraintType = field(
        init=False, default=ConstraintType.FOREIGN_KEY
    )
    referenced_table: str
    column_mapping: dict[str, str] = field(
        hash=False
    )  # maps the corresponding column names: {referencing_column1: referenced_column1, ...}


@dataclass(frozen=True)
class CheckConstraint(TableWideConstraint):
    """Class for the CHECK constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.CHECK)
    condition: str


@dataclass(frozen=True)
class DefaultConstraint(ColumnWideConstraint):
    """Class for the DEFAULT constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.DEFAULT)
    value: str
