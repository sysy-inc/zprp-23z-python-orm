import os

import pytest
from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.studio.utils.db_config_dynamic_import import (
    db_config_dynamic_import,
)


def write_temp_schema_file(file_path: str, file_content: str):
    with open(file_path, "w") as f:
        f.write(file_content)


def test_db_config_dynamic_import_normal():
    schema_file = (
        os.getcwd() + "/tmp/test_schema_test_db_config_dynamic_import_normal.py"
    )
    write_temp_schema_file(
        file_path=schema_file,
        file_content="""from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
SQLite3Config(db_path="some/path/to/db.db")""",
    )
    db_config = db_config_dynamic_import(schema_file_path=schema_file)

    assert isinstance(db_config, SQLite3Config)
    assert db_config.db_path == "some/path/to/db.db"
    assert BaseDbConfig.get_instance() == db_config


def test_db_config_dynamic_import_file_not_exists():
    schema_file = os.getcwd() + "/tmp/not_existant.py"
    with pytest.raises(FileNotFoundError):
        db_config_dynamic_import(schema_file_path=schema_file)


def test_db_config_dynamic_import_schema_path_is_not_file():
    schema_file = os.getcwd()
    with pytest.raises(TypeError):
        db_config_dynamic_import(schema_file_path=schema_file)
