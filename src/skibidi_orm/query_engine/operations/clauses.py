"""
Module representing differnet types of clauses present in where statement
for example equal, greater than, ...
"""
from typing import Any
from abc import ABC


class Clause(ABC):
    def __init__(self, column: str, val: Any) -> None:
        self._col = column
        self._val = val

    @property
    def col(self):
        return self._col

    @property
    def val(self):
        return self._val

    @property
    def type(self):
        return self.__class__


class Eq(Clause):
    pass
