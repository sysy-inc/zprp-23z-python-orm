"""
Representation of result from query to database
"""
from typing import Any


class Result:
    """
    Represents a result from a query to a database.

    Attributes:
        data (dict[str, Any]): A dictionary containing the data retrieved from the database.
    """
    def __init__(self, data: dict[str, Any]):
        """
        Initializes a Result object with the provided data.

        Args:
            data (dict[str, Any]): A dictionary containing the data retrieved from the database.
        """
        self.__dict__.update(data.items())
