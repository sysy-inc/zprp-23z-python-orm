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

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.constraint_type.value}', '{self.table_name}')"


@dataclass(frozen=True, repr=False)
class ColumnSpecificConstraint(Constraint):
    """Base class for constraints that apply to a column instead of multiple (e.g. composite foreign keys)"""

    column_name: str

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.constraint_type.value}', '{self.column_name}')"


@dataclass(frozen=True, repr=False)
class NotNullConstraint(ColumnSpecificConstraint):
    """Class for the NOT NULL constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.NOT_NULL)


@dataclass(frozen=True, repr=False)
class UniqueConstraint(ColumnSpecificConstraint):
    """Class for the UNIQUE constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.UNIQUE)


@dataclass(frozen=True, repr=False)
class PrimaryKeyConstraint(ColumnSpecificConstraint):
    """Class for the PRIMARY KEY constraint"""

    constraint_type: ConstraintType = field(
        init=False, default=ConstraintType.PRIMARY_KEY
    )


@dataclass(frozen=True, unsafe_hash=True, repr=False)
class ForeignKeyConstraint(Constraint):
    """Class for the FOREIGN KEY constraint"""

    constraint_type: ConstraintType = field(
        init=False, default=ConstraintType.FOREIGN_KEY
    )
    referenced_table: str
    column_mapping: dict[str, str] = field(
        hash=False
    )  # maps the corresponding column names: {referencing_column1: referenced_column1, ...}

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.constraint_type.value}', '{self.table_name}', '{self.referenced_table}', {self.column_mapping})"


@dataclass(frozen=True, repr=False)
class CheckConstraint(ColumnSpecificConstraint):
    """Class for the CHECK constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.CHECK)
    condition: str

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.constraint_type.value}', '{self.column_name}', '{self.condition}')"


@dataclass(frozen=True, repr=False)
class DefaultConstraint(ColumnSpecificConstraint):
    """Class for the DEFAULT constraint"""

    constraint_type: ConstraintType = field(init=False, default=ConstraintType.DEFAULT)
    value: str

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.constraint_type.value}', '{self.column_name}', '{self.value}')"
