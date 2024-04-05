import pytest

from skibidi_orm.migration_engine.db_config.base_config import (
    BaseDbConfig,
    ConfigSingleton,
)


@pytest.fixture(autouse=True)
def reset_config_singleton(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(ConfigSingleton, "_instances", {})
    monkeypatch.setattr(BaseDbConfig, "_BaseDbConfig__instances_count", 0)
