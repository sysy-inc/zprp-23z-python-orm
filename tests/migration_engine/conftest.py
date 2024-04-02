import pytest

from skibidi_orm.migration_engine.config import DbConfig
from skibidi_orm.migration_engine.utils import SingletonMeta


@pytest.fixture(autouse=True)
def reset_config_singleton(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(SingletonMeta, "_instances", {})
    monkeypatch.setattr(DbConfig, "_DbConfig__instances_count", 0)
