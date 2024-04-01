import os
from pathlib import Path
import shutil
import pytest
from skibidi_orm.migration_engine.config import SQLite3Config
from skibidi_orm.migration_engine.db_inspector import SqliteInspector
import sqlite3


class TestSQLite3Inspector:
    temp_dir = "./tmp"
    temp_db_file1 = "./tmp/test_db_inspectors.db"

    @pytest.fixture(autouse=True)
    def make_database(self):
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

        os.mkdir(self.temp_dir)
        Path(self.temp_db_file1).touch()
        conn = sqlite3.connect(self.temp_db_file1)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE table1 (id INTEGER PRIMARY KEY, name TEXT);")
        cursor.execute("CREATE TABLE table2 (id INTEGER PRIMARY KEY, name TEXT);")
        conn.commit()
        cursor.close()
        conn.close()
        yield
        shutil.rmtree(self.temp_dir)

    def test_can_only_be_instantiated_with_sqlite3config_instantiated_earlier(self):
        with pytest.raises(ReferenceError) as exc_info:
            SqliteInspector()
        assert str(exc_info.value) == "Instance does not exist"

    def test_get_tables_names(self):
        SQLite3Config(db_path=self.temp_db_file1)
        inspector = SqliteInspector()
        # @Pyright ignore
        tables = inspector.get_tables_names()  # type: ignore
        assert len(tables) == 2
        assert tables[0] == "table1"
        assert tables[1] == "table2"
