from typing import Any


class SingletonMeta(type):
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    @staticmethod
    def instance_exists(class_name: Any) -> bool:
        return class_name in SingletonMeta._instances
