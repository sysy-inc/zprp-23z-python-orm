from typing import Any, Callable
from skibidi_orm.migration_engine.utils import SingletonMeta


class DbConfig:
    __instances_count = 0

    @classmethod
    def instance(cls):
        if not SingletonMeta.instance_exists(cls):
            raise ReferenceError("Instance does not exist")
        return cls()

    def __init_subclass__(cls) -> None:
        cls.__init__ = DbConfig.__modify_init(cls.__init__)

    @staticmethod
    def __modify_init(init_func: Callable[[Any], Any]):
        def wrapper(*args: Any, **kwargs: Any):
            if DbConfig.__instances_count > 0:
                raise RuntimeError("Only one instance of this class is allowed")
            DbConfig.__instances_count += 1
            init_func(*args, **kwargs)

        return wrapper


class SQLite3Config(DbConfig, metaclass=SingletonMeta):
    """
    Configuration class for SQLite3 database.
    Instantiating it means choosing SQLite3 as the database.
    """

    def __init__(self, db_path: str):
        self.__db_path = db_path

    @property
    def db_path(self):
        return self.__db_path


class PostgresConfig(DbConfig, metaclass=SingletonMeta):
    def __init__(self, db_path: str):
        self.db_path = db_path
