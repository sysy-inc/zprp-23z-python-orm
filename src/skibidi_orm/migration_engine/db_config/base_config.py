from __future__ import annotations
from typing import Any, Self


class BaseDbConfig:
    """
    Base class for all database configurations.
    Ensures that only one instance of all subclasses of this class can be created.
    """

    __instance: Any = None

    @classmethod
    def get_instance(cls) -> Self:
        if BaseDbConfig.__instance is None:
            raise ReferenceError("Instance does not exist")
        return BaseDbConfig.__instance

    def __init_subclass__(cls) -> None:
        """
        Ensures that only one instance of all subclasses of this class can be created.
        """
        cls.__new__ = BaseDbConfig.__modify_new(cls)

    @staticmethod
    def __modify_new(class_t: Any):
        old_new = class_t.__new__

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if BaseDbConfig.__instance is not None:
                raise RuntimeError("Only one instance of this class is allowed")
            BaseDbConfig.__instance = old_new(class_t)
            return BaseDbConfig.__instance

        return wrapper
