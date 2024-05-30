import importlib

from fastapi.testclient import TestClient
import pytest
from skibidi_orm.migration_engine.data_mutator.sqlite3_data_mutatorr import (
    SQLite3DataMutator,
)
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import (
    SQLite3Inspector,
)
from skibidi_orm.migration_engine.studio.server import app
import pathlib


client = TestClient(app)

sql_schema_with_fks = [
    """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""",
    """
    CREATE TABLE posts (
        post_id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );
""",
    """
    CREATE TABLE comments (
        comment_id INTEGER PRIMARY KEY,
        user_idd INTEGER NOT NULL,
        post_id INTEGER NOT NULL,
        comment_text TEXT NOT NULL,
        comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_idd) REFERENCES users(user_id),
        FOREIGN KEY (post_id) REFERENCES posts(post_id)
    );
""",
]

sql_simple_db = [
    """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE
    );
"""
]


@pytest.mark.parametrize("make_database", [[*sql_simple_db]], indirect=True)
def test_GET_db(
    monkeypatch: pytest.MonkeyPatch, tmp_path: pathlib.Path, make_database: str
):
    import skibidi_orm.migration_engine.studio.server  # type: ignore

    importlib.import_module("skibidi_orm.migration_engine.studio.server")

    SQLite3Config(db_path=make_database)
    monkeypatch.setattr(
        "skibidi_orm.migration_engine.studio.server.db_inspector",
        SQLite3Inspector(),
    )
    response = client.get("/db")
    assert response.status_code == 200
    assert sorted(response.json()) == sorted(
        {
            "tables": [
                {
                    "name": "users",
                    "columns": [
                        {
                            "constraints": [
                                {
                                    "constraint_type": "PRIMARY KEY",
                                    "column_name": "username",
                                    "table_name": "users",
                                }
                            ],
                            "data_type": "INTEGER",
                            "name": "user_id",
                        },
                        {
                            "data_type": "TEXT",
                            "name": "username",
                            "constraints": [
                                {
                                    "constraint_type": "NOT NULL",
                                    "column_name": "username",
                                    "table_name": "users",
                                }
                            ],
                        },
                    ],
                }
            ]
        }
    )


@pytest.mark.parametrize("make_database", [[*sql_simple_db]], indirect=True)
def test_POST_route_db_table_name_row_correct(
    monkeypatch: pytest.MonkeyPatch, make_database: str
):
    import skibidi_orm.migration_engine.studio.server  # type: ignore

    importlib.import_module("skibidi_orm.migration_engine.studio.server")

    SQLite3Config(db_path=make_database)
    monkeypatch.setattr(
        "skibidi_orm.migration_engine.studio.server.db_inspector",
        SQLite3Inspector(),
    )
    monkeypatch.setattr(
        "skibidi_orm.migration_engine.studio.server.db_mutator",
        SQLite3DataMutator(),
    )
    response = client.post(
        "/db/users/row",
        json={
            "row": [
                {"name": "user_id", "value": "1"},
                {"name": "username", "value": "test"},
            ]
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Row inserted successfully."}
