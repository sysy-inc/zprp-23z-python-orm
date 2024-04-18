# from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
# from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
# from skibidi_orm.migration_engine.migration_element import MigrationElement
# from skibidi_orm.migration_engine.operations import constraints as C
# from skibidi_orm.migration_engine.operations.column_operations import (
#     AddColumnOperation,
#     DeleteColumnOperation,
# )
# from skibidi_orm.migration_engine.operations.table_operations import (
#     CreateTableOperation,
#     DeleteTableOperation,
#     RenameTableOperation,
# )

# from pathlib import Path
# import pytest
# import sqlite3

# sql_table_user = """
#     CREATE TABLE User (
#         user_id INTEGER PRIMARY KEY,
#         user_name TEXT NOT NULL
#     );
# """
# sql_table_post = """
#     CREATE TABLE Post (
#         post_id INTEGER PRIMARY KEY,
#         post_name TEXT NOT NULL
#     );
# """

# sql_table_comment = """
#     CREATE TABLE Comment (
#         comment_id INTEGER PRIMARY KEY,
#         comment_name TEXT NOT NULL
#     );
# """

# sql_table_primary_key_not_null = """
#     CREATE TABLE table_primary_key_not_null (
#         id INTEGER PRIMARY KEY NOT NULL
#     );
# """


# def execute_sqlite3_commands(db_path: str, commands: list[str]):
#     """Executes the given commands in a SQLite DB living under db_path"""
#     with sqlite3.connect(db_path) as conn:
#         cursor = conn.cursor()
#         for command in commands:
#             cursor.execute(command)
#         conn.commit()
#         cursor.close()


# @pytest.fixture
# def tmp_database(request: pytest.FixtureRequest, tmp_path: Path):
#     """Fixture for creating a temporary database and executing sqlite3 code. Yields the
#     path of the db file."""
#     sql_commands = request.param
#     (tmp_file := tmp_path.joinpath("tmp_db.db")).touch()
#     execute_sqlite3_commands(
#         str(tmp_file),
#         sql_commands,
#     )
#     yield str(tmp_file)


# @pytest.mark.parametrize(
#     "tmp_database", [[sql_table_user, sql_table_post]], indirect=True
# )
# def test_create_table_operation_needed(
#     tmp_database: str, capfd: pytest.CaptureFixture[str]
# ):

#     class Table(MigrationElement):

#         def __init__(self) -> None:
#             self.adapter = SQLite3Adapter()

#             models = Table.__subclasses__()
#             if self.__class__ == Table:
#                 for cls in models:
#                     self.adapter.create_table(cls.__dict__["table"])

#     class User(Table):  # type: ignore
#         columns = [
#             SQLite3Adapter.Column(
#                 name="user_id",
#                 data_type="INTEGER",
#                 constraints=[C.PrimaryKeyConstraint("User", "user_id")],
#             ),
#             SQLite3Adapter.Column(
#                 name="user_name",
#                 data_type="TEXT",
#                 constraints=[C.NotNullConstraint("User", "user_name")],
#             ),
#         ]

#         table = SQLite3Adapter.Table(name="User", columns=columns)

#     class Post(Table):  # type: ignore
#         columns = [
#             SQLite3Adapter.Column(
#                 name="post_id",
#                 data_type="INTEGER",
#                 constraints=[C.PrimaryKeyConstraint("Post", "post_id")],
#             ),
#             SQLite3Adapter.Column(
#                 name="post_name",
#                 data_type="TEXT",
#                 constraints=[C.NotNullConstraint("Post", "post_name")],
#             ),
#         ]

#         table = SQLite3Adapter.Table(name="Post", columns=columns)

#     class Comment(Table):  # type: ignore

#         columns = [
#             SQLite3Adapter.Column(
#                 name="comment_id",
#                 data_type="INTEGER",
#                 constraints=[C.PrimaryKeyConstraint("Comment", "comment_id")],
#             ),
#             SQLite3Adapter.Column(
#                 name="comment_name",
#                 data_type="TEXT",
#                 constraints=[C.NotNullConstraint("Comment", "comment_name")],
#             ),
#         ]

#         table = SQLite3Adapter.Table(name="Comment", columns=columns)

#     SQLite3Config(tmp_database)

#     m = MigrationElement()
#     m.migrate()

#     assert type(MigrationElement.operations[0]) == CreateTableOperation
#     assert len(MigrationElement.operations) == 1
