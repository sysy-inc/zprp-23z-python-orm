import pytest
from skibidi_orm.migration_engine.data_mutator.sqlite3_data_mutatorr import (
    SQLite3DataMutator,
)
from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.studio.utils.get_db_seeder import get_db_mutator


def test_get_db_seeder_sqlite3_error_when_config_not_exists():
    with pytest.raises(ReferenceError):
        get_db_mutator(db_config=BaseDbConfig.get_instance())


def test_get_db_seeder_sqlite3():
    seeder = get_db_mutator(db_config=SQLite3Config(db_path="some/path/to/db.db"))
    assert isinstance(seeder, SQLite3DataMutator)
