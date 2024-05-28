"""
Representation of result from query to database
"""
from typing import Any

class Result:
    def __init__(self, data: dict[str, Any]):
            self.__dict__.update(data.items())
