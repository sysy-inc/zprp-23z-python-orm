import sqlite3
from typing import Any
from colorama import Style
import pytest

from skibidi_orm.migration_engine.db_config.base_config import (
    BaseDbConfig,
)
import py  # type: ignore


@pytest.fixture(autouse=True)
def reset_config_singleton(monkeypatch: pytest.MonkeyPatch):
    # monkeypatch.setattr(ConfigSingleton, "_instances", {})
    # monkeypatch.setattr(BaseDbConfig, "_BaseDbConfig__instances_count", 0)
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


def execute_sqlite3_commands(db_path: str, commands: list[str]):
    """Executes the given commands in a SQLite DB living under db_path"""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        conn.commit()
        cursor.close()


@pytest.fixture
def make_database(request: pytest.FixtureRequest, tmpdir: py.path.local):
    sql_commands = (
        request.__getattribute__("param") if hasattr(request, "param") else None
    )
    p = tmpdir.join("temp_db.db")  # type: ignore
    p.write("")  # type: ignore
    if sql_commands:
        execute_sqlite3_commands(
            p.strpath,  # type: ignore
            sql_commands,
        )
    yield p
    tmpdir.remove()
