from skibidi_orm.migration_engine.adapters.providers import DatabaseProvider
from skibidi_orm.migration_engine.db_config.base_config import (
    BaseDbConfig,
)


class PostgresConfig(BaseDbConfig):

    database_provider = DatabaseProvider.POSTGRESQL

    def __init__(self, db_path: str):
        self.db_path = db_path
