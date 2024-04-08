from typing import Any
from colorama import Style
import pytest

from skibidi_orm.migration_engine.db_config.base_config import (
    BaseDbConfig,
)


@pytest.fixture(autouse=True)
def reset_config_singleton(monkeypatch: pytest.MonkeyPatch):
    # monkeypatch.setattr(ConfigSingleton, "_instances", {})
    # monkeypatch.setattr(BaseDbConfig, "_BaseDbConfig__instances_count", 0)
    monkeypatch.setattr(BaseDbConfig, "_BaseDbConfig__instance", None)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: Any) -> Any:
    outcome: Any = yield
    report = outcome.get_result()
    test_fn = item.obj
    docstring = getattr(test_fn, "__doc__")
    if docstring:
        docstring = docstring.strip()
        report.nodeid = Style.DIM + docstring + Style.RESET_ALL
