import os
from pathlib import Path
import shutil
from typing import Any
import pytest
from skibidi_orm.migration_engine.config import SQLite3Config
from skibidi_orm.migration_engine.db_inspector import SqliteInspector
import sqlite3


class TestSQLite3Inspector:
    temp_dir = "./tmp"
    temp_db_file = "./tmp/test_db_inspectors.db"

    def __create_temp_db_file(self, temp_dir: str, db_file: str):
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

        os.mkdir(temp_dir)
        Path(db_file).touch()

    def __execute_sqlite3_commands(self, db_path: str, commands: list[str]):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        conn.commit()
        cursor.close()
        conn.close()

    def __delete_temp_db_file(self, temp_dir: str):
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    @pytest.fixture
    def make_database(self) -> Any:
        self.__create_temp_db_file(self.temp_dir, self.temp_db_file)
        self.__execute_sqlite3_commands(
            self.temp_db_file,
            [
                """
            CREATE TABLE table1 (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            """,
                """
            CREATE TABLE table2 (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL
            );
            """,
            ],
        )
        x: Any = yield
        print(x, "CHUJCHUJ")
        self.__delete_temp_db_file(self.temp_dir)

    @pytest.mark.usefixtures("make_database")
    def test_can_only_be_instantiated_with_sqlite3config_instantiated_earlier(self):
        with pytest.raises(ReferenceError) as exc_info:
            SqliteInspector()
        assert str(exc_info.value) == "Instance does not exist"

    @pytest.mark.usefixtures("make_database")
    def test_get_tables_names(self):
        SQLite3Config(db_path=self.temp_db_file)
        inspector = SqliteInspector()
        tables = inspector.get_tables_names()  # type: ignore
        assert len(tables) == 2
        assert tables[0] == "table1"
        assert tables[1] == "table2"

    @pytest.mark.usefixtures("make_database")
    def test_get_table_columns(self):
        SQLite3Config(db_path=self.temp_db_file)
        inspector = SqliteInspector()
        inspector.get_table_columns("table1")
