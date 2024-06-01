import pathlib
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite.sqlite3_inspector import (
    SQLite3Inspector,
)
from skibidi_orm.migration_engine.studio.utils.get_db_inspector import get_db_inspector
import py  # type: ignore


def write_temp_schema_file(file_path: str, file_content: str):
    with open(file_path, "w") as f:
        f.write(file_content)


def test_get_db_inspector_sqlite3(tmp_path: pathlib.Path):
    p = tmp_path.joinpath("schema_test_get_db_inspector_sqlite3.py")
    p.write_text(
        """from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
SQLite3Config(db_path="some/path/to/db.db")"""
    )
    db_inspector = get_db_inspector(
        db_config=SQLite3Config(db_path="some/path/to/db.db")
    )
    assert isinstance(db_inspector, SQLite3Inspector)
