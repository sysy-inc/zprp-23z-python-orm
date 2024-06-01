from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig
from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector
from skibidi_orm.migration_engine.db_inspectors.postgres_inspector import (
    PostgresInspector,
)
from skibidi_orm.migration_engine.db_inspectors.sqlite.sqlite3_inspector import (
    SQLite3Inspector,
)


def get_db_inspector(db_config: BaseDbConfig) -> BaseDbInspector:
    if isinstance(db_config, SQLite3Config):
        return SQLite3Inspector()
    elif isinstance(db_config, PostgresConfig):
        return PostgresInspector()

    raise NotImplementedError
