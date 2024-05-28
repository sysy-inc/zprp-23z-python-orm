"""
Module describing agregate functions like COUNT
"""
from abc import ABC

class Function(ABC):
    def __init__(self, column: str) -> None:
        super().__init__()
        self._col = column
    
    @property
    def column(self):
        return self._col
    
    @property
    def type(self):
        return self.__class__
    

class Count(Function):
    pass
