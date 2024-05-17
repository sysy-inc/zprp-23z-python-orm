import os
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import SqliteInspector
from skibidi_orm.migration_engine.studio.utils.get_db_inspector import get_db_inspector


def write_temp_schema_file(file_path: str, file_content: str):
    with open(file_path, "w") as f:
        f.write(file_content)


def test_get_db_inspector_sqlite3():
    schema_file = os.getcwd() + "/tmp/test_schema_test_get_db_inspector_sqlite3.py"
    write_temp_schema_file(
        file_path=schema_file,
        file_content="""from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
SQLite3Config(db_path="some/path/to/db.db")""",
    )
    db_inspector = get_db_inspector(schema_file=schema_file)
    assert isinstance(db_inspector, SqliteInspector)
