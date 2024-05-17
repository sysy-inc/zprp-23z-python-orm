import pytest
from skibidi_orm.migration_engine.data_mutator.sqlite3_data_mutatorr import (
    SQLite3DataMutator,
)
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import SqliteInspector
from skibidi_orm.migration_engine.studio.utils.get_db_seeder import get_db_seeder


def test_get_db_seeder_sqlite3_error_when_config_not_exists():
    with pytest.raises(ReferenceError):
        get_db_seeder(db_inspector=SqliteInspector())


def test_get_db_seeder_sqlite3():
    SQLite3Config(db_path="some/path/to/db.db")
    seeder = get_db_seeder(db_inspector=SqliteInspector())
    assert isinstance(seeder, SQLite3DataMutator)
