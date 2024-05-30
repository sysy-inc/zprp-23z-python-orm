from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import (
    SQLite3Inspector,
)
from skibidi_orm.migration_engine.studio.utils.db_config_dynamic_import import (
    db_config_dynamic_import,
)


def get_db_inspector(schema_file: str) -> BaseDbInspector:
    db_config = db_config_dynamic_import(schema_file_path=schema_file)
    if isinstance(db_config, SQLite3Config):
        return SQLite3Inspector()
    elif isinstance(db_config, PostgresConfig):
        raise NotImplementedError

    raise NotImplementedError
