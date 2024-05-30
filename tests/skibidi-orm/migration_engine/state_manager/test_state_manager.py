from skibidi_orm.migration_engine.adapters.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor

from skibidi_orm.migration_engine.adapters.database_objects import constraints as c
from skibidi_orm.migration_engine.operations.column_operations import (
    AddColumnOperation,
    DeleteColumnOperation,
)
from skibidi_orm.migration_engine.operations.table_operations import (
    CreateTableOperation,
    DeleteTableOperation,
    RenameTableOperation,
)

from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)

# from tmp.mock_schema import Table

from pathlib import Path
import pytest
import sqlite3

sql_table_user = """
    CREATE TABLE User (
        user_id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL
    );
"""
sql_table_post = """
    CREATE TABLE Post (
        post_id INTEGER PRIMARY KEY,
        post_name TEXT NOT NULL
    );
"""

sql_table_comment = """
    CREATE TABLE Comment (
        comment_id INTEGER PRIMARY KEY,
        comment_name TEXT NOT NULL
    );
"""

sql_table_primary_key_not_null = """
    CREATE TABLE table_primary_key_not_null (
        id INTEGER PRIMARY KEY NOT NULL
    );
"""


# TODO: what is this?
# sql_schema_with_fks = [
#     """
#     CREATE TABLE users (
#         user_id INTEGER PRIMARY KEY,
#         username TEXT NOT NULL UNIQUE,
#         email TEXT NOT NULL UNIQUE,
#         password_hash TEXT NOT NULL,
#         registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     );
# """,
#     """
#     CREATE TABLE posts (
#         post_id INTEGER PRIMARY KEY,
#         user_id INTEGER NOT NULL,
#         title TEXT NOT NULL,
#         content TEXT NOT NULL,
#         post_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY (user_id) REFERENCES users(user_id)
#     );
# """,
#     """
#     CREATE TABLE comments (
#         comment_id INTEGER PRIMARY KEY,
#         user_idd INTEGER NOT NULL,
#         post_id INTEGER NOT NULL,
#         comment_text TEXT NOT NULL,
#         comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#         FOREIGN KEY (user_idd) REFERENCES users(user_id),
#         FOREIGN KEY (post_id) REFERENCES posts(post_id)
#     );
# """,
# ]


def execute_sqlite3_commands(db_path: str, commands: list[str]):
    """Executes the given commands in a SQLite DB living under db_path"""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for command in commands:
            cursor.execute(command)
        conn.commit()
        cursor.close()


@pytest.fixture
def tmp_database(request: pytest.FixtureRequest, tmp_path: Path):
    """Fixture for creating a temporary database and executing sqlite3 code. Yields the
    path of the db file."""
    sql_commands = request.param
    (tmp_file := tmp_path.joinpath("tmp_db.db")).touch()
    execute_sqlite3_commands(
        str(tmp_file),
        sql_commands,
    )
    yield str(tmp_file)


@pytest.fixture
def mock_execute_operations(monkeypatch: pytest.MonkeyPatch):
    # Define a function that does nothing
    def do_nothing(operations):  # type: ignore
        print("do_nothing")
        pass

    # Patch the execute_operations method with the do_nothing function
    monkeypatch.setattr(
        SQLite3Executor,
        "execute_operations",
        do_nothing,  # type: ignore
    )


@pytest.mark.parametrize(
    "tmp_database", [[sql_table_user, sql_table_post]], indirect=True
)
def test_rename_table_operation_needed(
    tmp_database: str, capfd: pytest.CaptureFixture[str]
):
    from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
        MigrationElement,
    )

    class Table(MigrationElement):

        def __init__(self) -> None:
            self.adapter = SQLite3Adapter()

            models = Table.__subclasses__()
            if self.__class__ == Table:
                for cls in models:
                    self.adapter.create_table(cls.__dict__["table"])

    class User(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="user_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("User", "user_id")],
            ),
            SQLite3Typing.Column(
                name="user_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("User", "user_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="User", columns=columns)

    class NewNamePost(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="post_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("NewNamePost", "post_id")],
            ),
            SQLite3Typing.Column(
                name="post_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("NewNamePost", "post_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="NewNamePost", columns=columns)

    SQLite3Config(tmp_database)

    m = MigrationElement()
    m.migrate(preview=True)

    assert type(MigrationElement.operations[0]) == RenameTableOperation
    assert len(MigrationElement.operations) == 1


@pytest.mark.parametrize(
    "tmp_database", [[sql_table_user, sql_table_post]], indirect=True
)
def test_no_operation_needed(
    tmp_database: str, mock_execute_operations: pytest.MonkeyPatch
):
    # TODO: refactor to avoid duplicating the setup multiple times
    class Table(MigrationElement):

        def __init__(self) -> None:
            self.adapter = SQLite3Adapter()

            models = Table.__subclasses__()
            if self.__class__ == Table:
                for cls in models:
                    self.adapter.create_table(cls.__dict__["table"])

    class User(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="user_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("User", "user_id")],
            ),
            SQLite3Typing.Column(
                name="user_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("User", "user_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="User", columns=columns)

    class Post(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="post_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("Post", "post_id")],
            ),
            SQLite3Typing.Column(
                name="post_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("Post", "post_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="Post", columns=columns)

    SQLite3Config(tmp_database)

    m = MigrationElement()
    m.migrate(preview=True)

    assert len(MigrationElement.operations) == 0


@pytest.mark.parametrize(
    "tmp_database", [[sql_table_user, sql_table_post]], indirect=True
)
def test_create_table_operation_needed(
    tmp_database: str, mock_execute_operations: pytest.MonkeyPatch
):

    class Table(MigrationElement):

        def __init__(self) -> None:
            self.adapter = SQLite3Adapter()

            models = Table.__subclasses__()
            if self.__class__ == Table:
                for cls in models:
                    self.adapter.create_table(cls.__dict__["table"])

    class User(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="user_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("User", "user_id")],
            ),
            SQLite3Typing.Column(
                name="user_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("User", "user_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="User", columns=columns)

    class Post(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="post_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("Post", "post_id")],
            ),
            SQLite3Typing.Column(
                name="post_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("Post", "post_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="Post", columns=columns)

    class Comment(Table):  # type: ignore

        columns = [
            SQLite3Typing.Column(
                name="comment_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("Comment", "comment_id")],
            ),
            SQLite3Typing.Column(
                name="comment_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("Comment", "comment_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="Comment", columns=columns)

    SQLite3Config(tmp_database)

    m = MigrationElement()
    m.migrate(preview=True)

    assert type(MigrationElement.operations[0]) == CreateTableOperation
    assert len(MigrationElement.operations) == 1


@pytest.mark.parametrize(
    "tmp_database", [[sql_table_user, sql_table_post, sql_table_comment]], indirect=True
)
def test_delete_table_operation_needed(
    tmp_database: str, mock_execute_operations: pytest.MonkeyPatch
):

    class Table(MigrationElement):

        def __init__(self) -> None:
            self.adapter = SQLite3Adapter()

            models = Table.__subclasses__()
            if self.__class__ == Table:
                for cls in models:
                    self.adapter.create_table(cls.__dict__["table"])

    class User(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="user_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("User", "user_id")],
            ),
            SQLite3Typing.Column(
                name="user_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("User", "user_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="User", columns=columns)

    class Post(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="post_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("Post", "post_id")],
            ),
            SQLite3Typing.Column(
                name="post_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("Post", "post_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="Post", columns=columns)

    SQLite3Config(tmp_database)

    m = MigrationElement()
    m.migrate(preview=True)

    assert len(MigrationElement.operations) == 1
    assert type(MigrationElement.operations[0]) == DeleteTableOperation


@pytest.mark.parametrize(
    "tmp_database", [[sql_table_user, sql_table_post]], indirect=True
)
def test_create_column_operation_needed(
    tmp_database: str, mock_execute_operations: pytest.MonkeyPatch
):

    class Table(MigrationElement):

        def __init__(self) -> None:
            self.adapter = SQLite3Adapter()

            models = Table.__subclasses__()
            if self.__class__ == Table:
                for cls in models:
                    self.adapter.create_table(cls.__dict__["table"])

    class User(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="user_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("User", "user_id")],
            ),
            SQLite3Typing.Column(
                name="user_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("User", "user_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="User", columns=columns)

    class Post(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="post_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("Post", "post_id")],
            ),
            SQLite3Typing.Column(
                name="post_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("Post", "post_name")],
            ),
            SQLite3Typing.Column(
                name="post_content",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("Post", "post_content")],
            ),
        ]

        table = SQLite3Typing.Table(name="Post", columns=columns)

    SQLite3Config(tmp_database)

    m = MigrationElement()
    m.migrate(preview=True)

    assert type(MigrationElement.operations[0]) == AddColumnOperation
    assert len(MigrationElement.operations) == 1


@pytest.mark.parametrize(
    "tmp_database", [[sql_table_user, sql_table_post]], indirect=True
)
def test_delete_column_operation_needed(
    tmp_database: str, mock_execute_operations: pytest.MonkeyPatch
):

    class Table(MigrationElement):

        def __init__(self) -> None:
            self.adapter = SQLite3Adapter()

            models = Table.__subclasses__()
            if self.__class__ == Table:
                for cls in models:
                    self.adapter.create_table(cls.__dict__["table"])

    class User(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="user_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("User", "user_id")],
            ),
            SQLite3Typing.Column(
                name="user_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("User", "user_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="User", columns=columns)

    class Post(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="post_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("Post", "post_id")],
            ),
        ]

        table = SQLite3Typing.Table(name="Post", columns=columns)

    SQLite3Config(tmp_database)

    m = MigrationElement()
    m.migrate(preview=True)

    assert type(MigrationElement.operations[0]) == DeleteColumnOperation
    assert len(MigrationElement.operations) == 1


@pytest.mark.parametrize(
    "tmp_database", [[sql_table_user, sql_table_post, sql_table_comment]], indirect=True
)
def test_add_column_and_delete_tabe_operation_needed(
    tmp_database: str, mock_execute_operations: pytest.MonkeyPatch
):
    class Table(MigrationElement):

        def __init__(self) -> None:
            self.adapter = SQLite3Adapter()

            models = Table.__subclasses__()
            if self.__class__ == Table:
                for cls in models:
                    self.adapter.create_table(cls.__dict__["table"])

    class User(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="user_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("User", "user_id")],
            ),
            SQLite3Typing.Column(
                name="user_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("User", "user_name")],
            ),
        ]

        table = SQLite3Typing.Table(name="User", columns=columns)

    class Post(Table):  # type: ignore
        columns = [
            SQLite3Typing.Column(
                name="post_id",
                data_type="INTEGER",
                column_constraints=[c.PrimaryKeyConstraint("Post", "post_id")],
            ),
            SQLite3Typing.Column(
                name="post_name",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("Post", "post_name")],
            ),
            SQLite3Typing.Column(
                name="post_content",
                data_type="TEXT",
                column_constraints=[c.NotNullConstraint("Post", "post_content")],
            ),
        ]

        table = SQLite3Typing.Table(name="Post", columns=columns)

    SQLite3Config(tmp_database)

    m = MigrationElement()
    m.migrate(preview=True)

    assert type(MigrationElement.operations[1]) == AddColumnOperation
    assert type(MigrationElement.operations[0]) == DeleteTableOperation

    assert len(MigrationElement.operations) == 2
