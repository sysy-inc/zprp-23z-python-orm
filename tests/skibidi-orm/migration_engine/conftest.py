import os
from pathlib import Path
import shutil
import sqlite3
from typing import Any
from colorama import Style
import pytest

from skibidi_orm.migration_engine.db_config.base_config import (
    BaseDbConfig,
)


@pytest.fixture(autouse=True)
def reset_config_singleton(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(BaseDbConfig, "_BaseDbConfig__instance", None)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Any) -> Any:
    """Print tests' docstring when running the test."""
    outcome: Any = yield
    report = outcome.get_result()
    test_fn = item.obj
    docstring = getattr(test_fn, "__doc__")
    if docstring:
        docstring = docstring.strip()
        report.nodeid = Style.DIM + docstring + Style.RESET_ALL


def recreate_temp_db_file(temp_dir: str, db_file: str):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.mkdir(temp_dir)
    Path(db_file).touch()


def delete_temp_db_dir(temp_dir: str):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


def execute_sqlite3_commands(db_path: str, commands: list[str]):
    """Executes the given commands in a SQLite DB living under db_path"""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        conn.commit()
        cursor.close()


@pytest.fixture
def make_database(request: pytest.FixtureRequest):
    sql_commands = (
        request.__getattribute__("param") if hasattr(request, "param") else None
    )
    recreate_temp_db_file("./tmp", "./tmp/temp_db.db")
    if sql_commands:
        execute_sqlite3_commands(
            "./tmp/temp_db.db",
            sql_commands,
        )
    yield "./tmp/temp_db.db"
    delete_temp_db_dir("./tmp")
