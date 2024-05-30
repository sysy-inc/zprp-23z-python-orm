"""
Module for defining aggregate functions like COUNT.
"""
from abc import ABC


class Function(ABC):
    """
    Abstract base class for defining aggregate functions.

    Attributes:
        _col (str): The column name on which the aggregate function operates.
    """
    def __init__(self, column: str) -> None:
        """
        Initializes an aggregate function with the given column name.

        Args:
            column (str): The column name on which the aggregate function operates.
        """
        super().__init__()
        self._col = column

    @property
    def column(self):
        """
        Returns the column name on which the aggregate function operates.

        Returns:
            str: The column name.
        """
        return self._col

    @property
    def type(self):
        """
        Returns the type of the aggregate function.

        Returns:
            Type[Function]: The type of the aggregate function.
        """
        return self.__class__


class Count(Function):
    """
    Represents the COUNT aggregate function.

    Inherits:
        Function: Abstract base class for defining aggregate functions.
    """
    pass
