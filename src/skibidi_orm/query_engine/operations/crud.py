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
        self._obj: Model = obj

    def table(self) -> str:
        """
        Returns the table name from the database.

        Returns:
            str: The table name.
        """
        table_name: str = self._obj._get_name_and_pk()[0]   # type: ignore
        return table_name   # type: ignore


class ValueBase(CRUDBase):
    """
    Base class for operations involving values (INSERT, UPDATE).

    Attributes:
        _attributes (list[tuple[str, Any]]): List of attribute-value pairs.
    """
    def __init__(self, obj: Model) -> None:
        self._attributes: list[tuple[str, Any]] = obj._get_attr_values()    # type: ignore
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
        self._returns: bool = obj._is_pk_none()     # type: ignore
        self._returning_col: list[str] = []
        if self._returns:
            self._returning_col: list[str] = [obj._get_db_pk()[0]]      # type: ignore
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
        atr = obj._update_changes_db()     # type: ignore
        atr_list = list(zip(atr.keys(), atr.values()))
        self._attributes = atr_list

    def where_clause(self) -> tuple[Eq]:
        """
        Returns the WHERE clause for the Update statement.

        Returns:
            tuple[Eq]: The tuple containing the WHERE clause.
        """
        pk_name, pk_value = self._obj._get_db_pk()      # type: ignore
        clause = Eq(pk_name, pk_value)  # type: ignore
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
        pk_name, pk_value = self._obj._get_db_pk()      # type: ignore
        clause = Eq(pk_name, pk_value)  # type: ignore
        return (clause, )
