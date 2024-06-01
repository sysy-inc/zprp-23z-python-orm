from skibidi_orm.migration_engine.data_mutator.base_data_mutator import BaseDataMutator
from skibidi_orm.migration_engine.data_mutator.postgres_data_mutator import (
    PostgresDataMutator,
)
from skibidi_orm.migration_engine.data_mutator.sqlite3_data_mutatorr import (
    SQLite3DataMutator,
)
from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig
from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config


def get_db_mutator(db_config: BaseDbConfig) -> BaseDataMutator:
    if isinstance(db_config, SQLite3Config):
        return SQLite3DataMutator()
    elif isinstance(db_config, PostgresConfig):
        return PostgresDataMutator()

    raise NotImplementedError
