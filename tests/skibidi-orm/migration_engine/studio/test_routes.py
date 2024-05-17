import importlib
from fastapi.testclient import TestClient
import pytest
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import SqliteInspector
from skibidi_orm.migration_engine.studio.server import app


client = TestClient(app)


def test_GET_db(monkeypatch: pytest.MonkeyPatch):
    # import skibidi_orm.migration_engine.studio.server  # type: ignore

    # module = importlib.import_module("skibidi_orm.migration_engine.studio.server")
    # print(module.__dict__)
    return
    SQLite3Config(db_path="./tmp/test_GET_db.db")
    # db_inspector = SqliteInspector()  # type: ignore
    # monkeypatch.setattr(
    #     "skibidi_orm.migration_engine.studio.server.db_inspector",
    #     SqliteInspector(),
    # )
    response = client.get("/db")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {"tables": []}
