import sqlite3
import pytest

from skibidi_orm.exceptions.db_mutator_exceptions import AmbigiousDeleteRowError
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    NotNullConstraint,
    PrimaryKeyConstraint,
)
from skibidi_orm.migration_engine.adapters.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.data_mutator.base_data_mutator import (
    DeleteRowPk,
    InsertRowColumn,
)
from skibidi_orm.migration_engine.data_mutator.sqlite3_data_mutatorr import (
    SQLite3DataMutator,
)
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import (
    SQLite3Inspector,
)

sql_simple_db = [
    """
    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY,
        username TEXT NOT NULL
    );
"""
]

sql_double_pk_db = [
    """
    CREATE TABLE Orders (
        order_id INTEGER,
        product_id INTEGER,
        PRIMARY KEY (order_id, product_id)
    );
"""
]

sql_simple_insert = [
    """
    INSERT INTO users (user_id, username) VALUES
    (1, 'test1'),
    (2, 'test2'),
    (3, 'test3')
;
"""
]


@pytest.mark.parametrize("make_database", [[*sql_simple_db]], indirect=True)
def test_insert_row(make_database: str):
    SQLite3Config(db_path=make_database)
    db_seeder = SQLite3DataMutator()
    db_seeder.insert_row(
        table_name="users",
        row=[
            InsertRowColumn(name="user_id", value=str(1)),
            InsertRowColumn(name="username", value="test"),
        ],
    )
    db_inspector = SQLite3Inspector()
    tables = db_inspector.get_tables()

    assert tables[0] == SQLite3Typing.Table(
        name="users",
        columns=[
            SQLite3Typing.Column(
                name="user_id",
                data_type="INTEGER",
                column_constraints=[
                    PrimaryKeyConstraint(table_name="users", column_name="user_id"),
                ],
            ),
            SQLite3Typing.Column(
                name="username",
                data_type="TEXT",
                column_constraints=[
                    NotNullConstraint(table_name="users", column_name="username"),
                ],
            ),
        ],
    )


@pytest.mark.parametrize("make_database", [[*sql_simple_db]], indirect=True)
def test_delete_row_one_pk(make_database: str):
    config = SQLite3Config(db_path=make_database)
    db_seeder = SQLite3DataMutator()

    db_seeder.insert_row(
        table_name="users",
        row=[
            InsertRowColumn(name="user_id", value=str(1)),
            InsertRowColumn(name="username", value="test"),
        ],
    )

    with sqlite3.connect(config.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        cursor.close()

    assert len(data) == 1

    db_seeder.delete_row(
        table_name="users",
        pks=[
            DeleteRowPk(name="user_id", value=str(1)),
        ],
    )

    with sqlite3.connect(config.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        cursor.close()

    assert len(data) == 0


@pytest.mark.parametrize("make_database", [[*sql_double_pk_db]], indirect=True)
def test_delete_row_two_pk(make_database: str):
    config = SQLite3Config(db_path=make_database)
    db_seeder = SQLite3DataMutator()
    db_seeder.insert_row(
        table_name="Orders",
        row=[
            InsertRowColumn(name="order_id", value=str(1)),
            InsertRowColumn(name="product_id", value=str(2)),
        ],
    )

    with sqlite3.connect(config.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Orders")
        data = cursor.fetchall()
        cursor.close()

    assert len(data) == 1

    db_seeder.delete_row(
        table_name="Orders",
        pks=[
            DeleteRowPk(name="order_id", value=str(1)),
            DeleteRowPk(name="product_id", value=str(2)),
        ],
    )

    with sqlite3.connect(config.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Orders")
        data = cursor.fetchall()
        cursor.close()

    assert len(data) == 0


@pytest.mark.parametrize("make_database", [[*sql_double_pk_db]], indirect=True)
def test_delete_row_table_two_pk_one_pk_given_ok(make_database: str):
    config = SQLite3Config(db_path=make_database)
    db_seeder = SQLite3DataMutator()
    db_seeder.insert_row(
        table_name="Orders",
        row=[
            InsertRowColumn(name="order_id", value=str(1)),
            InsertRowColumn(name="product_id", value=str(1)),
        ],
    )
    db_seeder.insert_row(
        table_name="Orders",
        row=[
            InsertRowColumn(name="order_id", value=str(1)),
            InsertRowColumn(name="product_id", value=str(2)),
        ],
    )

    with sqlite3.connect(config.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Orders")
        data = cursor.fetchall()
        cursor.close()

    assert len(data) == 2

    db_seeder.delete_row(
        table_name="Orders",
        pks=[
            DeleteRowPk(name="product_id", value=str(2)),
        ],
    )

    with sqlite3.connect(config.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Orders")
        data = cursor.fetchall()
        cursor.close()

    assert len(data) == 1
    assert data[0] == (1, 1)


@pytest.mark.parametrize("make_database", [[*sql_double_pk_db]], indirect=True)
def test_delete_row_table_two_pk_two_pk_given_ok(make_database: str):
    config = SQLite3Config(db_path=make_database)
    db_seeder = SQLite3DataMutator()
    db_seeder.insert_row(
        table_name="Orders",
        row=[
            InsertRowColumn(name="order_id", value=str(1)),
            InsertRowColumn(name="product_id", value=str(1)),
        ],
    )
    db_seeder.insert_row(
        table_name="Orders",
        row=[
            InsertRowColumn(name="order_id", value=str(1)),
            InsertRowColumn(name="product_id", value=str(2)),
        ],
    )

    with sqlite3.connect(config.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Orders")
        data = cursor.fetchall()
        cursor.close()

    assert len(data) == 2

    db_seeder.delete_row(
        table_name="Orders",
        pks=[
            DeleteRowPk(name="order_id", value=str(1)),
            DeleteRowPk(name="product_id", value=str(2)),
        ],
    )

    with sqlite3.connect(config.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Orders")
        data = cursor.fetchall()
        cursor.close()

    assert len(data) == 1
    assert data[0] == (1, 1)


@pytest.mark.parametrize("make_database", [[*sql_double_pk_db]], indirect=True)
def test_delete_row_table_two_pk_one_pk_given_ambigious(make_database: str):
    config = SQLite3Config(db_path=make_database)
    db_seeder = SQLite3DataMutator()
    db_seeder.insert_row(
        table_name="Orders",
        row=[
            InsertRowColumn(name="order_id", value=str(1)),
            InsertRowColumn(name="product_id", value=str(1)),
        ],
    )
    db_seeder.insert_row(
        table_name="Orders",
        row=[
            InsertRowColumn(name="order_id", value=str(1)),
            InsertRowColumn(name="product_id", value=str(2)),
        ],
    )

    with sqlite3.connect(config.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Orders")
        data = cursor.fetchall()
        cursor.close()

    assert len(data) == 2

    with pytest.raises(AmbigiousDeleteRowError):
        db_seeder.delete_row(
            table_name="Orders",
            pks=[
                DeleteRowPk(name="order_id", value=str(1)),
            ],
        )


@pytest.mark.parametrize(
    "make_database", [[*sql_simple_db, *sql_simple_insert]], indirect=True
)
def test_raw_query(make_database: str):
    SQLite3Config(db_path=make_database)
    db_mutator = SQLite3DataMutator()
    data = db_mutator.raw_query("SELECT * FROM users;")
    assert data == [(1, "test1"), (2, "test2"), (3, "test3")]


@pytest.mark.parametrize(
    "make_database", [[*sql_simple_db, *sql_simple_insert]], indirect=True
)
def test_get_rows_normal(make_database: str):
    SQLite3Config(db_path=make_database)
    db_mutator = SQLite3DataMutator()
    data = db_mutator.get_rows("users")
    assert data == [(1, "test1"), (2, "test2"), (3, "test3")]


@pytest.mark.parametrize(
    "make_database", [[*sql_simple_db, *sql_simple_insert]], indirect=True
)
def test_get_rows_offset(make_database: str):
    SQLite3Config(db_path=make_database)
    db_mutator = SQLite3DataMutator()
    data = db_mutator.get_rows("users", offset=1)
    assert data == [(2, "test2"), (3, "test3")]
    data = db_mutator.get_rows("users", offset=2)
    assert data == [(3, "test3")]
    data = db_mutator.get_rows("users", offset=3)
    assert data == []


@pytest.mark.parametrize(
    "make_database", [[*sql_simple_db, *sql_simple_insert]], indirect=True
)
def test_get_rows_limit(make_database: str):
    SQLite3Config(db_path=make_database)
    db_mutator = SQLite3DataMutator()
    data = db_mutator.get_rows("users", limit=1)
    assert data == [(1, "test1")]
    data = db_mutator.get_rows("users", limit=2)
    assert data == [(1, "test1"), (2, "test2")]
    data = db_mutator.get_rows("users", limit=3)
    assert data == [(1, "test1"), (2, "test2"), (3, "test3")]
    data = db_mutator.get_rows("users", limit=4)
    assert data == [(1, "test1"), (2, "test2"), (3, "test3")]
