"""
The CRUD module provides classes for generating SQL statements
for CRUD (Insert, Update, Delete) operations on database tables.
"""

from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.operations.clauses import Eq
from typing import Any


class CRUDBase:
    """
    Base class for generating SQL statements for INSERT, UPDATE, and DELETE operations.

    Attributes:
        _obj (Model): The model object associated with the CRUD operation.
    """
    def __init__(self, obj: Model) -> None:
        """
        Initializes a CRUDBase object with the given object.

        Args:
            obj (Model): The model object to create CRUD operation.
        """
        self._obj = None

    def table(self) -> str:
        """
        Returns the table name from the database.

        Returns:
            str: The table name.
        """
        # table_name = self._obj.table() need to be implemented in Model
        table_name = "test_model"   # temporarly TOCHANGE
        return table_name


class ValueBase(CRUDBase):
    """
    Base class for operations involving values (INSERT, UPDATE).

    Attributes:
        _attributes (list[tuple[str, Any]]): List of attribute-value pairs.
    """
    def __init__(self, obj: Model) -> None:
        # self._attributes = obj.attributes() need to be implemented in Model
        self._attributes: list[tuple[str, Any]] = [("id", 1), ("atr1", 1), ("atr2", "a")]  # temporarly TOCHANGE
        super().__init__(obj)

    def values(self) -> list[Any]:
        """
        Returns the list of values to be inserted or updated.

        Returns:
            list[Any]: The list of values.
        """
        return [attr[1] for attr in self._attributes]

    def columns(self) -> list[str]:
        """
        Returns the list of column names.

        Returns:
            list[str]: The list of column names.
        """
        return [attr[0] for attr in self._attributes]

    def attributes(self) -> list[tuple[str, Any]]:
        """
        Returns the list of attribute-value pairs.

        Returns:
            list[tuple[str, Any]]: The list of attribute-value pairs.
        """
        return self._attributes


class Insert(ValueBase):
    """
    Represents an Insert statement.

    Attributes:
        _returns (bool): Indicates if the statement returns values.
        _returning_col (list[str]): List of column names to return.
    """
    def __init__(self, obj: Model) -> None:
        """
        Initializes an Insert statement.

        Args:
            obj (Model): The model object associated with the Insert statement.
        """
        # self._returns: bool = obj.check_primary_key() to be implemented in Model
        self._returns: bool = True  # temporarly TOCHANGE
        # self._returning: list[str] = obj.primary_key() to be implemented in Model
        self._returning_col: list[str] = ["id"]  # temporarly TOCHANGE
        super().__init__(obj)

    @property
    def returns(self) -> bool:
        """
        Returns whether the statement returns values.

        Returns:
            bool: True if values are returned, False otherwise.
        """
        return self._returns

    @property
    def returning_col(self) -> list[str]:
        """
        Returns the list of column names to return.

        Returns:
            list[str]: The list of column names.
        """
        return self._returning_col


class Update(ValueBase):
    """
    Represents an Update statement.
    """
    def __init__(self, obj: Model) -> None:
        """
        Initializes an Update statement.

        Args:
            obj (Model): The model object associated with the Update statement.
        """
        super().__init__(obj)
        # TODO get attributes that are changed
        self._attributes = [("atr1", 4)]

    def where_clause(self) -> tuple[Eq]:
        """
        Returns the WHERE clause for the Update statement.

        Returns:
            tuple[Eq]: The tuple containing the WHERE clause.
        """
        # primary_key = self._obj.primary_key() to be implementd in Model
        clause = Eq("id", 1)  # temporarly TOCHANGE
        return (clause, )


class Delete(CRUDBase):
    """
    Represents a Delete statement.
    """
    def __init__(self, obj: Model) -> None:
        """
        Initializes a Delete statement.

        Args:
            obj (Model): The model object associated with the Delete statement.
        """
        super().__init__(obj)

    def where_clause(self) -> tuple[Eq]:
        """
        Returns the WHERE clause for the Delete statement.

        Returns:
            tuple[Eq]: The tuple containing the WHERE clause.
        """
        # primary_key = self._obj.primary_key() to be implementd in Model
        clause = Eq("id", 1)  # temporarly TOCHANGE
        return (clause, )
