"""
Module describing SELECT statement
"""
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.operations import clauses as c
from skibidi_orm.query_engine.operations.clauses import Clause
from skibidi_orm.query_engine.operations.functions import Function
from typing import Type, Any


class Select:
    def __init__(self, model_class: Type[Model]) -> None:
        self._table: str = model_class._meta.db_table      # type: ignore # TODO change it to function
        self._model = model_class
        self._fields: list[str | Function] = ["id", "atr1", "atr2"]     # type: ignore # TODO function in model
        self._where_clauses: list[Clause] = []
        self._group_by_col: list[str] = []
        self._order_by_col: list[str] = []
        self._order_by_desc: bool = False
        self._returns_model: bool = True    # if it returns model or only specific columns
        self._annotations: dict[str | Function, str] = {}

    @property
    def fields(self):
        return self._fields

    @property
    def table(self):
        return self._table

    @property
    def where_clauses(self):
        return self._where_clauses

    @property
    def group_by_col(self):
        return self._group_by_col

    @property
    def order_by_col(self):
        return self._order_by_col, self._order_by_desc

    @property
    def returning_model(self):
        return self._returns_model

    @property
    def annotations(self):
        return self._annotations

    @property
    def model(self):
        return self._model

    def filter(self, **kwargs: Any):
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
                    # TODO maybe change this Error
                    raise SyntaxError("Invalid option with column name")

        return self

    def group_by(self, *args: str):
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
        for val in args:
            self._order_by_col.append(val)
        self._order_by_desc = desc
        return self

    def annotate(self, **kwargs: str | Function):
        self._returns_model = False
        for anotation, value in kwargs.items():
            if value not in self._fields:
                self._fields.append(value)
            self._annotations[value] = anotation
        return self
