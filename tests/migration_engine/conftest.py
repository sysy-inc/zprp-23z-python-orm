import pytest

from skibidi_orm.migration_engine.config import ConfigSingleton, DbConfig


@pytest.fixture(autouse=True)
def reset_config_singleton(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(ConfigSingleton, "_instances", {})
    monkeypatch.setattr(DbConfig, "_DbConfig__instances_count", 0)
