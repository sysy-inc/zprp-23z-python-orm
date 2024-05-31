"""
Module describing SELECT statement.
"""
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.operations import clauses as c
from skibidi_orm.query_engine.operations.clauses import Clause
from skibidi_orm.query_engine.operations.functions import Function
from typing import Type, Any


class Select:
    """
    Represents a SELECT query.

    Attributes:
        _table (str): The name of the database table.
        _model (Type[Model]): The model class representing the database table.
        _fields (list[str | Function]): The list of fields to select.
        _where_clauses (list[Clause]): The list of WHERE clauses for filtering.
        _group_by_col (list[str]): The list of columns for grouping.
        _order_by_col (list[str]): The list of columns for ordering.
        _order_by_desc (bool): Indicates whether ordering is descending.
        _returns_model (bool): Indicates whether the query returns a model or specific columns.
        _annotations (dict[str | Function, str]): The annotations for query columns.
    """
    def __init__(self, model_class: Type[Model]) -> None:
        """
        Initializes a SELECT query with the given model class.

        Args:
            model_class (Type[Model]): The model class representing the database table.
        """
        self._table: str = model_class._meta.db_table      # type: ignore
        self._model = model_class
        self._fields: list[str | Function] = model_class._get_columns_names()     # type: ignore
        self._where_clauses: list[Clause] = []
        self._group_by_col: list[str] = []
        self._order_by_col: list[str] = []
        self._order_by_desc: bool = False
        self._returns_model: bool = True
        self._annotations: dict[str | Function, str] = {}

    @property
    def fields(self):
        """
        Get the list of fields to select.

        Returns:
            list[str | Function]: The list of fields.
        """
        return self._fields

    @property
    def table(self):
        """
        Get the name of the database table.

        Returns:
            str: The table name.
        """
        return self._table

    @property
    def where_clauses(self):
        """
        Get the list of WHERE clauses for filtering.

        Returns:
            list[Clause]: The list of WHERE clauses.
        """
        return self._where_clauses

    @property
    def group_by_col(self):
        """
        Get the list of columns for grouping.

        Returns:
            list[str]: The list of columns for grouping.
        """
        return self._group_by_col

    @property
    def order_by_col(self):
        """
        Get the columns for ordering and the ordering direction.

        Returns:
            Tuple[list[str], bool]: A tuple containing the columns for ordering and a boolean indicating the ordering direction.
        """
        return self._order_by_col, self._order_by_desc

    @property
    def returning_model(self):
        """
        Check if the query returns a model or specific columns.

        Returns:
            bool: True if the query returns a model, False if it returns specific columns.
        """
        return self._returns_model

    @property
    def annotations(self):
        """
        Get the annotations for query columns.

        Returns:
            dict[str | Function, str]: The annotations for query columns.
        """
        return self._annotations

    @property
    def model(self):
        """
        Get the model class representing the database table.

        Returns:
            Type[Model]: The model class.
        """
        return self._model

    def filter(self, **kwargs: Any):
        """
        Adds filter conditions to the query.
        Possible options for filter conditions:
            - no option: equal
            - __gt: greater than
            - __gte: greater than or equal
            - __lt: lower than
            - __lte: lower than or equal
            - __not: not equal
            - __isnull: if True is Null, if False is not Null

        Args:
            **kwargs: Keyword arguments representing filter conditions.

        Returns:
            Select: The Select instance with filter conditions added.

        Examples:
            Select(User).filter(name="Thom", id__gt=1)
        """
        for arg_name, arg_value in kwargs.items():
            # check if __ is present in name
            if "__" not in arg_name:
                # there are no special options it is equal clause
                self._where_clauses.append(c.Eq(arg_name, arg_value))
            else:
                # it has some special options
                name, operation = arg_name.split("__")
                if operation == "gt":
                    self._where_clauses.append(c.Gt(name, arg_value))
                elif operation == "gte":
                    self._where_clauses.append(c.GtEq(name, arg_value))
                elif operation == "lt":
                    self._where_clauses.append(c.Lt(name, arg_value))
                elif operation == "lte":
                    self._where_clauses.append(c.LtEq(name, arg_value))
                elif operation == "not":
                    self._where_clauses.append(c.NotEq(name, arg_value))
                elif operation == "isnull":
                    if arg_value:
                        # it is set to True
                        self._where_clauses.append(c.Null(name, None))
                    else:
                        # it is set to False
                        self._where_clauses.append(c.NotNull(name, None))
                else:
                    # invalid option
                    raise SyntaxError("Invalid option")

        return self

    def group_by(self, *args: str):
        """
        Adds grouping to the query.

        Args:
            *args: list of columns for grouping.

        Returns:
            Select: The Select instance with grouping added.

        Examples:
            Select(User).group_by("id")
        """
        self._fields = []   # reset fields list
        if self._annotations:
            self._fields.extend(self._annotations.keys())

        self._returns_model = False     # returns specific columns
        for val in args:
            self._group_by_col.append(val)
            if val not in self._fields:
                self._fields.append(val)
        return self

    def order_by(self, *args: str, desc: bool = False):
        """
        Adds ordering to the query.

        Args:
            *args: list of columns for ordering.
            desc (bool, optional): Indicates whether ordering is descending. Defaults to False.

        Returns:
            Select: The Select instance with ordering added.

        Examples:
            Select(User).order_by("id", desc=True)
        """
        for val in args:
            self._order_by_col.append(val)
        self._order_by_desc = desc
        return self

    def annotate(self, **kwargs: str | Function):
        """
        Adds annotations to the query.

        Args:
            **kwargs: Keyword arguments representing annotations.

        Returns:
            Select: The Select instance with annotations added.

        Examples:
            Select(User).annotate(new_name="original_column_name")
        """
        self._returns_model = False
        for anotation, value in kwargs.items():
            if value not in self._fields:
                self._fields.append(value)
            self._annotations[value] = anotation
        return self
