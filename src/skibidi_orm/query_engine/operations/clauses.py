"""
Module representing differnet types of clauses present in where statement
for example equal, greater than, ...
"""
from typing import Any
from abc import ABC


class Clause(ABC):
    """
    Abstract base class representing a generic clause.

    Attributes:
        col (str): The column name involved in the clause.
        val (Any): The value involved in the clause.
        type (type): The type of the clause.
    """
    def __init__(self, column: str, val: Any) -> None:
        """
        Initializes a Clause object with the given column name and value.

        Args:
            column (str): The column name involved in the clause.
            val (Any): The value associated with the column.
        """
        self._col = column
        self._val = val

    @property
    def col(self):
        """
        str: The column name involved in the clause.
        """
        return self._col

    @property
    def val(self):
        """
        Any: The value involved in the clause.
        """
        return self._val

    @property
    def type(self):
        """
        type: The type of the clause.
        """
        return self.__class__


class Eq(Clause):
    """
    Represents an equality clause (==).

    Inherits:
        Clause: Abstract base class representing a generic clause.
    """
    pass

class NotEq(Clause):
    """
    Represents a not-equal clause (!=).

    Inherits:
        Clause: Abstract base class representing a generic clause.
    """
    pass

class Gt(Clause):
    """
    Represents a greater-than clause (>).

    Inherits:
        Clause: Abstract base class representing a generic clause.
    """
    pass

class GtEq(Clause):
    """
    Represents a greater-than-or-equal clause (>=).

    Inherits:
        Clause: Abstract base class representing a generic clause.
    """
    pass

class Lt(Clause):
    """
    Represents a less-than clause (<).

    Inherits:
        Clause: Abstract base class representing a generic clause.
    """
    pass

class LtEq(Clause):
    """
    Represents a less-than-or-equal clause (<=).

    Inherits:
        Clause: Abstract base class representing a generic clause.
    """
    pass

class Null(Clause):
    """
    Represents an is-null clause (is Null).

    Inherits:
        Clause: Abstract base class representing a generic clause.
    """
    pass

class NotNull(Clause):
    """
    Represents an is-not-null clause (is not Null).

    Inherits:
        Clause: Abstract base class representing a generic clause.
    """
    pass
