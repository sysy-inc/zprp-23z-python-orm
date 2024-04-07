from typing import Any, Callable


class ConfigSingleton(type):
    _instances: dict[Any, Any] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

    @staticmethod
    def instance_exists(class_name: Any) -> bool:
        return class_name in ConfigSingleton._instances


class BaseDbConfig:
    """
    Base class for all database configurations.
    Ensures that only one instance of all subclasses of this class can be created.
    """

    __instances_count = 0

    @classmethod
    def get_instance(cls):
        if not ConfigSingleton.instance_exists(cls):
            raise ReferenceError("Instance does not exist")
        return cls()

    def __init_subclass__(cls) -> None:
        """
        Ensures that only one instance of all subclasses of this class can be created.
        """
        cls.__init__ = BaseDbConfig.__modify_init(cls.__init__)

    @staticmethod
    def __modify_init(init_func: Callable[[Any], Any]):
        def wrapper(*args: Any, **kwargs: Any):
            if BaseDbConfig.__instances_count > 0:
                raise RuntimeError("Only one instance of this class is allowed")
            BaseDbConfig.__instances_count += 1
            init_func(*args, **kwargs)

        return wrapper
