from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import (
    SQLite3Inspector,
)
from skibidi_orm.migration_engine.studio.utils.get_db_inspector import get_db_inspector
import py  # type: ignore


def write_temp_schema_file(file_path: str, file_content: str):
    with open(file_path, "w") as f:
        f.write(file_content)


def test_get_db_inspector_sqlite3(tmpdir: py.path.local):
    p = tmpdir.join("schema_test_get_db_inspector_sqlite3.py")  # type: ignore
    p.write(  # type: ignore
        """from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
SQLite3Config(db_path="some/path/to/db.db")"""
    )
    db_inspector = get_db_inspector(schema_file=p.strpath)  # type: ignore
    assert isinstance(db_inspector, SQLite3Inspector)
    tmpdir.remove()
