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


class Constraint(ABC):
    """Base class for all constraints"""

    constraint_type: ConstraintType = field(init=False)
    table_name: str
    column_name: str


@dataclass(frozen=True)
class NotNullConstraint(Constraint):
    """Class for the NOT NULL constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.NOT_NULL)


@dataclass(frozen=True)
class UniqueConstraint(Constraint):
    """Class for the UNIQUE constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.UNIQUE)


@dataclass(frozen=True)
class PrimaryKeyConstraint(Constraint):
    """Class for the PRIMARY KEY constraint"""

    constraint_type: ConstraintType = field(
        init=False, default=ConstraintType.PRIMARY_KEY
    )


@dataclass(frozen=True)
class ForeignKeyConstraint(Constraint):
    """Class for the FOREIGN KEY constraint"""

    constraint_type: ConstraintType = field(
        init=False, default=ConstraintType.FOREIGN_KEY
    )
    referenced_table: str
    column_mapping: dict[
        str, str
    ]  # maps the names of corresponding columns from both tables (in case of composite foreign keys)


@dataclass(frozen=True)
class CheckConstraint(Constraint):
    """Class for the CHECK constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.CHECK)
    condition: str


@dataclass(frozen=True)
class DefaultConstraint(Constraint):
    """Class for the DEFAULT constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.DEFAULT)
    value: str
