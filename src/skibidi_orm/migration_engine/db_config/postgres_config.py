from skibidi_orm.migration_engine.db_config.base_config import (
    BaseDbConfig,
    ConfigSingleton,
)


class PostgresConfig(BaseDbConfig, metaclass=ConfigSingleton):
    def __init__(self, db_path: str):
        self.db_path = db_path
