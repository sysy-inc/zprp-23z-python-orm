from abc import ABC
import enum
from dataclasses import dataclass, field


class ConstraintType(enum.Enum):
    """All supported constraint types"""

    NOT_NULL = enum.auto()
    UNIQUE = enum.auto()
    PRIMARY_KEY = enum.auto()
    FOREIGN_KEY = enum.auto()
    CHECK = enum.auto()
    DEFAULT = enum.auto()


@dataclass(frozen=True)
class Constraint(ABC):
    """Base class for all constraints"""

    constraint_type: ConstraintType = field(init=False)
    table_name: str


@dataclass(frozen=True)
class ColumnSpecificConstraint(Constraint):
    """Base class for constraints that apply to a column instead of multiple (e.g. composite foreign keys)"""

    column_name: str


@dataclass(frozen=True)
class NotNullConstraint(ColumnSpecificConstraint):
    """Class for the NOT NULL constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.NOT_NULL)


@dataclass(frozen=True)
class UniqueConstraint(ColumnSpecificConstraint):
    """Class for the UNIQUE constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.UNIQUE)


@dataclass(frozen=True)
class PrimaryKeyConstraint(ColumnSpecificConstraint):
    """Class for the PRIMARY KEY constraint"""

    constraint_type: ConstraintType = field(
        init=False, default=ConstraintType.PRIMARY_KEY
    )


@dataclass(frozen=True, unsafe_hash=True)
class ForeignKeyConstraint(Constraint):
    """Class for the FOREIGN KEY constraint"""

    constraint_type: ConstraintType = field(
        init=False, default=ConstraintType.FOREIGN_KEY
    )
    referenced_table: str
    column_mapping: dict[str, str] = field(
        hash=False
    )  # maps the corresponding column names: {referencing_column1: referenced_column1, ...}


@dataclass(frozen=True)
class CheckConstraint(ColumnSpecificConstraint):
    """Class for the CHECK constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.CHECK)
    condition: str


@dataclass(frozen=True)
class DefaultConstraint(ColumnSpecificConstraint):
    """Class for the DEFAULT constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.DEFAULT)
    value: str
