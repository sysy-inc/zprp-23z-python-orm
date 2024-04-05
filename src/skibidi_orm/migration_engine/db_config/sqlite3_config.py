from skibidi_orm.migration_engine.db_config.base_config import (
    BaseDbConfig,
    ConfigSingleton,
)


class SQLite3Config(BaseDbConfig, metaclass=ConfigSingleton):
    """
    Configuration class for SQLite3 database.
    Instantiating it means choosing SQLite3 as the database.
    """

    def __init__(self, db_path: str):
        self.__db_path = db_path

    @property
    def db_path(self):
        return self.__db_path
