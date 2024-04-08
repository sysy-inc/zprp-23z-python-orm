import os
from pathlib import Path
import shutil
import pytest
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import SqliteInspector
import sqlite3


temp_dir = "./tmp"
temp_db_file = "./tmp/test_db_inspectors.db"
sql_table1 = """
    CREATE TABLE table1 (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
"""
sql_table2 = """
    CREATE TABLE table2 (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
"""
sql_table_primary_key_not_null = """
    CREATE TABLE table_primary_key_not_null (
        id INTEGER PRIMARY KEY NOT NULL
    );
"""

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


def create_temp_db_file(temp_dir: str, db_file: str):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)

    os.mkdir(temp_dir)
    Path(db_file).touch()


def execute_sqlite3_commands(db_path: str, commands: list[str]):
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        conn.commit()
        cursor.close()


def delete_temp_db_file(temp_dir: str):
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def make_database(request: pytest.FixtureRequest):
    sql_commands = request.param
    create_temp_db_file(temp_dir, temp_db_file)
    execute_sqlite3_commands(
        temp_db_file,
        sql_commands,
    )
    yield
    delete_temp_db_file(temp_dir)


@pytest.mark.parametrize("make_database", [[sql_table1, sql_table2]], indirect=True)
@pytest.mark.usefixtures("make_database")
def test_can_only_be_instantiated_with_sqlite3config_instantiated_earlier():
    with pytest.raises(ReferenceError) as exc_info:
        SqliteInspector()
    assert str(exc_info.value) == "Instance does not exist"


@pytest.mark.parametrize("make_database", [[sql_table1, sql_table2]], indirect=True)
@pytest.mark.usefixtures("make_database")
def test_get_tables_names():
    SQLite3Config(db_path=temp_db_file)
    inspector = SqliteInspector()
    tables = inspector.get_tables_names()
    assert len(tables) == 2
    assert tables[0] == "table1"
    assert tables[1] == "table2"


@pytest.mark.parametrize("make_database", [[sql_table1, sql_table2]], indirect=True)
@pytest.mark.usefixtures("make_database")
def test_get_table_columns():
    SQLite3Config(db_path=temp_db_file)
    inspector = SqliteInspector()
    columns = inspector.get_table_columns("table1")
    assert columns[0].name == "id"
    assert columns[0].data_type == "INTEGER"
    assert columns[0].constraints == ["PRIMARY KEY"]
    assert columns[1].name == "name"
    assert columns[1].data_type == "TEXT"
    assert columns[1].constraints == ["NOT NULL"]
    assert len(columns) == 2


@pytest.mark.parametrize(
    "make_database", [[sql_table_primary_key_not_null]], indirect=True
)
@pytest.mark.usefixtures("make_database")
def test_get_table_columns__primaryk_notnull():
    SQLite3Config(db_path=temp_db_file)
    inspector = SqliteInspector()
    columns = inspector.get_table_columns("table_primary_key_not_null")
    assert columns[0].name == "id"
    assert columns[0].data_type == "INTEGER"
    assert columns[0].constraints == ["PRIMARY KEY", "NOT NULL"]


@pytest.mark.parametrize("make_database", [[sql_table1, sql_table2]], indirect=True)
@pytest.mark.usefixtures("make_database")
def test_get_tables():
    SQLite3Config(db_path=temp_db_file)
    inspector = SqliteInspector()
    tables = inspector.get_tables()
    assert len(tables) == 2
    assert tables[0].name == "table1"
    assert tables[1].name == "table2"
    assert len(tables[0].columns) == 2
    assert len(tables[1].columns) == 2
    assert tables[0].columns[0].name == "id"
    assert tables[0].columns[0].data_type == "INTEGER"
    assert tables[0].columns[0].constraints == ["PRIMARY KEY"]
    assert tables[0].columns[1].name == "name"
    assert tables[0].columns[1].data_type == "TEXT"
    assert tables[0].columns[1].constraints == ["NOT NULL"]
    assert tables[1].columns[0].name == "id"
    assert tables[1].columns[0].data_type == "INTEGER"
    assert tables[1].columns[0].constraints == ["PRIMARY KEY"]
    assert tables[1].columns[1].name == "name"
    assert tables[1].columns[1].data_type == "TEXT"
    assert tables[1].columns[1].constraints == ["NOT NULL"]


@pytest.mark.parametrize("make_database", [[*sql_schema_with_fks]], indirect=True)
@pytest.mark.usefixtures("make_database")
def test_get_relations():
    SQLite3Config(db_path=temp_db_file)
    inspector = SqliteInspector()
    relations = inspector.get_relations()
    assert len(relations) == 3
    posts_relation = list(filter(lambda rel: rel.origin_table == "posts", relations))[0]
    assert posts_relation.origin_table == "posts"
    assert posts_relation.origin_column == "user_id"
    assert posts_relation.referenced_table == "users"
    assert posts_relation.referenced_column == "user_id"
    comments_relation_user = list(
        filter(
            lambda rel: rel.origin_table == "comments"
            and rel.origin_column == "user_idd",
            relations,
        )
    )[0]
    assert comments_relation_user.origin_table == "comments"
    assert comments_relation_user.origin_column == "user_idd"
    assert comments_relation_user.referenced_table == "users"
    assert comments_relation_user.referenced_column == "user_id"
    comments_relation_post = list(
        filter(
            lambda rel: rel.origin_table == "comments"
            and rel.origin_column == "post_id",
            relations,
        )
    )[0]
    assert comments_relation_post.origin_table == "comments"
    assert comments_relation_post.origin_column == "post_id"
    assert comments_relation_post.referenced_table == "posts"
    assert comments_relation_post.referenced_column == "post_id"
