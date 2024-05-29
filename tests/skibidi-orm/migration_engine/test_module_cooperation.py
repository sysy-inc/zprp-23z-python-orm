from skibidi_orm.migration_engine.adapters.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import (
    SQLite3Inspector,
)
from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)
from skibidi_orm.migration_engine.adapters.database_objects import constraints as c
from .sql_data import SQLite3TablesData


def test_adding_table_to_database(make_database: str):
    SQLite3Config(make_database)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_user)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_post)

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

    m = MigrationElement()
    m.migrate()

    tables = SQLite3Inspector().get_tables()

    assert len(tables) == 3
    assert tables[2].name == "Comment"
    assert tables[2].columns[0].name == "comment_id"
    assert tables[2].columns[0].data_type == "INTEGER"
    assert tables[2].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("Comment", "comment_id")
    ]
    assert tables[2].columns[1].name == "comment_name"
    assert tables[2].columns[1].data_type == "TEXT"
    assert tables[2].columns[1].column_constraints == [
        c.NotNullConstraint("Comment", "comment_name")
    ]


def test_removing_table_from_database(make_database: str):
    SQLite3Config(make_database)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_user)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_post)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_comment)

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

    m = MigrationElement()
    m.migrate()

    tables = SQLite3Inspector().get_tables()

    tables.sort(key=lambda table: table.name, reverse=True)

    assert len(tables) == 2
    assert tables[0].name == "User"
    assert tables[0].columns[0].name == "user_id"
    assert tables[0].columns[0].data_type == "INTEGER"
    assert tables[0].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("User", "user_id")
    ]
    assert tables[0].columns[1].name == "user_name"
    assert tables[0].columns[1].data_type == "TEXT"
    assert tables[0].columns[1].column_constraints == [
        c.NotNullConstraint("User", "user_name")
    ]

    assert tables[1].name == "Post"
    assert tables[1].columns[0].name == "post_id"
    assert tables[1].columns[0].data_type == "INTEGER"
    assert tables[1].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("Post", "post_id")
    ]
    assert tables[1].columns[1].name == "post_name"
    assert tables[1].columns[1].data_type == "TEXT"
    assert tables[1].columns[1].column_constraints == [
        c.NotNullConstraint("Post", "post_name")
    ]


def test_add_column_to_database(make_database: str):
    SQLite3Config(make_database)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_user)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_post)

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

    m = MigrationElement()
    m.migrate()

    tables = SQLite3Inspector().get_tables()

    tables.sort(key=lambda table: table.name, reverse=True)

    assert len(tables) == 2
    assert tables[0].name == "User"
    assert tables[0].columns[0].name == "user_id"
    assert tables[0].columns[0].data_type == "INTEGER"
    assert tables[0].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("User", "user_id")
    ]
    assert tables[0].columns[1].name == "user_name"
    assert tables[0].columns[1].data_type == "TEXT"
    assert tables[0].columns[1].column_constraints == [
        c.NotNullConstraint("User", "user_name")
    ]

    assert tables[1].name == "Post"
    assert tables[1].columns[0].name == "post_id"
    assert tables[1].columns[0].data_type == "INTEGER"
    assert tables[1].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("Post", "post_id")
    ]
    assert tables[1].columns[1].name == "post_name"
    assert tables[1].columns[1].data_type == "TEXT"
    assert tables[1].columns[1].column_constraints == [
        c.NotNullConstraint("Post", "post_name")
    ]
    assert tables[1].columns[2].name == "post_content"
    assert tables[1].columns[2].data_type == "TEXT"
    assert tables[1].columns[2].column_constraints == [
        c.NotNullConstraint("Post", "post_content")
    ]


def test_removing_column_from_database(make_database: str):
    SQLite3Config(make_database)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_user)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_post)

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

    m = MigrationElement()
    m.migrate()

    tables = SQLite3Inspector().get_tables()

    tables.sort(key=lambda table: table.name, reverse=True)

    assert len(tables) == 2
    assert tables[0].name == "User"
    assert tables[0].columns[0].name == "user_id"
    assert tables[0].columns[0].data_type == "INTEGER"
    assert tables[0].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("User", "user_id")
    ]
    assert tables[0].columns[1].name == "user_name"
    assert tables[0].columns[1].data_type == "TEXT"
    assert tables[0].columns[1].column_constraints == [
        c.NotNullConstraint("User", "user_name")
    ]

    assert tables[1].name == "Post"
    assert len(tables[1].columns) == 1
    assert tables[1].columns[0].name == "post_id"
    assert tables[1].columns[0].data_type == "INTEGER"
    assert tables[1].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("Post", "post_id")
    ]


def test_renaming_table_in_database(make_database: str):
    SQLite3Config(make_database)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_user)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_post)

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

    m = MigrationElement()
    m.migrate()

    tables = SQLite3Inspector().get_tables()

    assert len(tables) == 2
    assert tables[0].name == "User"
    assert tables[0].columns[0].name == "user_id"
    assert tables[0].columns[0].data_type == "INTEGER"
    assert tables[0].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("User", "user_id")
    ]
    assert tables[0].columns[1].name == "user_name"
    assert tables[0].columns[1].data_type == "TEXT"
    assert tables[0].columns[1].column_constraints == [
        c.NotNullConstraint("User", "user_name")
    ]

    assert tables[1].name == "NewNamePost"
    assert tables[1].columns[0].name == "post_id"
    assert tables[1].columns[0].data_type == "INTEGER"
    assert tables[1].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("NewNamePost", "post_id")
    ]
    assert tables[1].columns[1].name == "post_name"
    assert tables[1].columns[1].data_type == "TEXT"
    assert tables[1].columns[1].column_constraints == [
        c.NotNullConstraint("NewNamePost", "post_name")
    ]


def test_add_column_to_database_and_remove_table_from_database(make_database: str):
    SQLite3Config(make_database)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_user)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_post)
    SQLite3Executor.execute_sql(SQLite3TablesData.sql_table_comment)

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

    m = MigrationElement()
    m.migrate()

    tables = SQLite3Inspector().get_tables()

    assert len(tables) == 2
    assert tables[0].name == "User"
    assert tables[0].columns[0].name == "user_id"
    assert tables[0].columns[0].data_type == "INTEGER"
    assert tables[0].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("User", "user_id")
    ]
    assert tables[0].columns[1].name == "user_name"
    assert tables[0].columns[1].data_type == "TEXT"
    assert tables[0].columns[1].column_constraints == [
        c.NotNullConstraint("User", "user_name")
    ]

    assert tables[1].name == "Post"
    assert tables[1].columns[0].name == "post_id"
    assert tables[1].columns[0].data_type == "INTEGER"
    assert tables[1].columns[0].column_constraints == [
        c.PrimaryKeyConstraint("Post", "post_id")
    ]
    assert tables[1].columns[1].name == "post_name"
    assert tables[1].columns[1].data_type == "TEXT"
    assert tables[1].columns[1].column_constraints == [
        c.NotNullConstraint("Post", "post_name")
    ]
    assert tables[1].columns[2].name == "post_content"
    assert tables[1].columns[2].data_type == "TEXT"
    assert tables[1].columns[2].column_constraints == [
        c.NotNullConstraint("Post", "post_content")
    ]
