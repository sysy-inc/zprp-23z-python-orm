"""
CRUD operations: INSERT, UPDATE, DELETE
"""

from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.operations.clauses import Eq
from typing import Any


class CRUDBase:
    """
    Base for INSERT, UPDATE, DELETE
    """
    def __init__(self, obj: Model) -> None:
        self._obj = None

    def table(self) -> str:
        """
        Return table name from database
        """
        # table_name = self._obj.table() need to be implemented in Model
        table_name = "test_model"   # temporarly TOCHANGE
        return table_name


class ValueBase(CRUDBase):
    """
    Base for operations involving values (INSERT, UPDATE)
    """
    def __init__(self, obj: Model) -> None:
        # self._attributes = obj.attributes() need to be implemented in Model
        self._attributes: list[tuple[str, Any]] = [("id", 1), ("atr1", 1), ("atr2", "a")]  # temporarly TOCHANGE
        super().__init__(obj)

    def values(self) -> list[Any]:
        return [attr[1] for attr in self._attributes]

    def columns(self) -> list[str]:
        return [attr[0] for attr in self._attributes]

    def attributes(self) -> list[tuple[str, Any]]:
        return self._attributes


class Insert(ValueBase):
    """
    Insert statement
    """
    def __init__(self, obj: Model) -> None:
        # self._returns: bool = obj.check_primary_key() to be implemented in Model
        self._returns: bool = True  # temporarly TOCHANGE
        # self._returning: list[str] = obj.primary_key() to be implemented in Model
        self._returning_col: list[str] = ["id"]  # temporarly TOCHANGE
        super().__init__(obj)

    @property
    def returns(self) -> bool:
        return self._returns

    @property
    def returning_col(self) -> list[str]:
        return self._returning_col


class Update(ValueBase):
    """
    Update statement
    """
    def __init__(self, obj: Model) -> None:
        super().__init__(obj)
        # TODO get attributes that are changed
        self._attributes = [("atr1", 4)]

    def where_clause(self) -> tuple[Eq]:
        # primary_key = self._obj.primary_key() to be implementd in Model
        clause = Eq("id", 1)  # temporarly TOCHANGE
        return (clause, )


class Delete(CRUDBase):
    """
    Delete statement
    """
    def __init__(self, obj: Model) -> None:
        super().__init__(obj)

    def where_clause(self) -> tuple[Eq]:
        # primary_key = self._obj.primary_key() to be implementd in Model
        clause = Eq("id", 1)  # temporarly TOCHANGE
        return (clause, )
