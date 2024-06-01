from skibidi_orm.migration_engine.adapters.providers import DatabaseProvider
from skibidi_orm.migration_engine.db_config.base_config import (
    BaseDbConfig,
)
import os


# TODO: make a dataclass out of config classes
class SQLite3Config(BaseDbConfig):
    """
    Configuration class for SQLite3 database.
    Instantiating it means choosing SQLite3 as the database.
    """

    database_provider = DatabaseProvider.SQLITE3

    def __init__(self, db_path: str):
        self.__db_path = os.path.abspath(db_path)

    @property
    def db_path(self) -> str:
        return self.__db_path
