from skibidi_orm.migration_engine.db_config.base_config import (
    BaseDbConfig,
)


class PostgresConfig(BaseDbConfig):
    def __init__(self, db_path: str):
        self.db_path = db_path
