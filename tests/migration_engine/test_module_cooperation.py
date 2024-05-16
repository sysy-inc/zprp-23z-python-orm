# from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
# from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import SqliteInspector
# from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor
# from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
# from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
#     MigrationElement,
# )
# from skibidi_orm.migration_engine.adapters.database_objects import constraints as C


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


# def test_adding_table_to_database(make_database: str):
#     SQLite3Config(make_database)
#     SQLite3Executor.execute_sql(sql_table_user)
#     SQLite3Executor.execute_sql(sql_table_post)

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

#     m = MigrationElement()
#     m.migrate()

#     tables = SqliteInspector().get_tables()

#     assert len(tables) == 3
#     assert tables[2].name == "Comment"
#     assert tables[2].columns[0].name == "comment_id"
#     assert tables[2].columns[0].data_type == "INTEGER"
#     assert tables[2].columns[0].constraints == [
#         C.PrimaryKeyConstraint("Comment", "comment_id")
#     ]
#     assert tables[2].columns[1].name == "comment_name"
#     assert tables[2].columns[1].data_type == "TEXT"
#     assert tables[2].columns[1].constraints == [
#         C.NotNullConstraint("Comment", "comment_name")
#     ]


# def test_removing_table_from_database(make_database: str):
#     SQLite3Config(make_database)
#     SQLite3Executor.execute_sql(sql_table_user)
#     SQLite3Executor.execute_sql(sql_table_post)
#     SQLite3Executor.execute_sql(sql_table_comment)

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

#     m = MigrationElement()
#     m.migrate()

#     tables = SqliteInspector().get_tables()

#     assert len(tables) == 2
#     assert tables[0].name == "User"
#     assert tables[0].columns[0].name == "user_id"
#     assert tables[0].columns[0].data_type == "INTEGER"
#     assert tables[0].columns[0].constraints == [
#         C.PrimaryKeyConstraint("User", "user_id")
#     ]
#     assert tables[0].columns[1].name == "user_name"
#     assert tables[0].columns[1].data_type == "TEXT"
#     assert tables[0].columns[1].constraints == [
#         C.NotNullConstraint("User", "user_name")
#     ]

#     assert tables[1].name == "Post"
#     assert tables[1].columns[0].name == "post_id"
#     assert tables[1].columns[0].data_type == "INTEGER"
#     assert tables[1].columns[0].constraints == [
#         C.PrimaryKeyConstraint("Post", "post_id")
#     ]
#     assert tables[1].columns[1].name == "post_name"
#     assert tables[1].columns[1].data_type == "TEXT"
#     assert tables[1].columns[1].constraints == [
#         C.NotNullConstraint("Post", "post_name")
#     ]


# def test_add_column_to_database(make_database: str):
#     SQLite3Config(make_database)
#     SQLite3Executor.execute_sql(sql_table_user)
#     SQLite3Executor.execute_sql(sql_table_post)

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
#             SQLite3Adapter.Column(
#                 name="post_content",
#                 data_type="TEXT",
#                 constraints=[C.NotNullConstraint("Post", "post_content")],
#             ),
#         ]

#         table = SQLite3Adapter.Table(name="Post", columns=columns)

#     m = MigrationElement()
#     m.migrate()

#     tables = SqliteInspector().get_tables()

#     assert len(tables) == 2
#     assert tables[0].name == "User"
#     assert tables[0].columns[0].name == "user_id"
#     assert tables[0].columns[0].data_type == "INTEGER"
#     assert tables[0].columns[0].constraints == [
#         C.PrimaryKeyConstraint("User", "user_id")
#     ]
#     assert tables[0].columns[1].name == "user_name"
#     assert tables[0].columns[1].data_type == "TEXT"
#     assert tables[0].columns[1].constraints == [
#         C.NotNullConstraint("User", "user_name")
#     ]

#     assert tables[1].name == "Post"
#     assert tables[1].columns[0].name == "post_id"
#     assert tables[1].columns[0].data_type == "INTEGER"
#     assert tables[1].columns[0].constraints == [
#         C.PrimaryKeyConstraint("Post", "post_id")
#     ]
#     assert tables[1].columns[1].name == "post_name"
#     assert tables[1].columns[1].data_type == "TEXT"
#     assert tables[1].columns[1].constraints == [
#         C.NotNullConstraint("Post", "post_name")
#     ]
#     assert tables[1].columns[2].name == "post_content"
#     assert tables[1].columns[2].data_type == "TEXT"
#     assert tables[1].columns[2].constraints == [
#         C.NotNullConstraint("Post", "post_content")
#     ]


# def test_removing_column_from_database(make_database: str):
#     SQLite3Config(make_database)
#     SQLite3Executor.execute_sql(sql_table_user)
#     SQLite3Executor.execute_sql(sql_table_post)

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
#         ]

#         table = SQLite3Adapter.Table(name="Post", columns=columns)

#     m = MigrationElement()
#     m.migrate()

#     tables = SqliteInspector().get_tables()

#     assert len(tables) == 2
#     assert tables[0].name == "User"
#     assert tables[0].columns[0].name == "user_id"
#     assert tables[0].columns[0].data_type == "INTEGER"
#     assert tables[0].columns[0].constraints == [
#         C.PrimaryKeyConstraint("User", "user_id")
#     ]
#     assert tables[0].columns[1].name == "user_name"
#     assert tables[0].columns[1].data_type == "TEXT"
#     assert tables[0].columns[1].constraints == [
#         C.NotNullConstraint("User", "user_name")
#     ]

#     assert tables[1].name == "Post"
#     assert len(tables[1].columns) == 1
#     assert tables[1].columns[0].name == "post_id"
#     assert tables[1].columns[0].data_type == "INTEGER"
#     assert tables[1].columns[0].constraints == [
#         C.PrimaryKeyConstraint("Post", "post_id")
#     ]


# def test_renaming_table_in_database(make_database: str):
#     SQLite3Config(make_database)
#     SQLite3Executor.execute_sql(sql_table_user)
#     SQLite3Executor.execute_sql(sql_table_post)

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

#     class NewNamePost(Table):  # type: ignore
#         columns = [
#             SQLite3Adapter.Column(
#                 name="post_id",
#                 data_type="INTEGER",
#                 constraints=[C.PrimaryKeyConstraint("NewNamePost", "post_id")],
#             ),
#             SQLite3Adapter.Column(
#                 name="post_name",
#                 data_type="TEXT",
#                 constraints=[C.NotNullConstraint("NewNamePost", "post_name")],
#             ),
#         ]

#         table = SQLite3Adapter.Table(name="NewNamePost", columns=columns)

#     m = MigrationElement()
#     m.migrate()

#     tables = SqliteInspector().get_tables()

#     assert len(tables) == 2
#     assert tables[0].name == "User"
#     assert tables[0].columns[0].name == "user_id"
#     assert tables[0].columns[0].data_type == "INTEGER"
#     assert tables[0].columns[0].constraints == [
#         C.PrimaryKeyConstraint("User", "user_id")
#     ]
#     assert tables[0].columns[1].name == "user_name"
#     assert tables[0].columns[1].data_type == "TEXT"
#     assert tables[0].columns[1].constraints == [
#         C.NotNullConstraint("User", "user_name")
#     ]

#     assert tables[1].name == "NewNamePost"
#     assert tables[1].columns[0].name == "post_id"
#     assert tables[1].columns[0].data_type == "INTEGER"
#     assert tables[1].columns[0].constraints == [
#         C.PrimaryKeyConstraint("NewNamePost", "post_id")
#     ]
#     assert tables[1].columns[1].name == "post_name"
#     assert tables[1].columns[1].data_type == "TEXT"
#     assert tables[1].columns[1].constraints == [
#         C.NotNullConstraint("NewNamePost", "post_name")
#     ]


# def test_add_column_to_database_and_remove_table_from_database(make_database: str):
#     SQLite3Config(make_database)
#     SQLite3Executor.execute_sql(sql_table_user)
#     SQLite3Executor.execute_sql(sql_table_post)
#     SQLite3Executor.execute_sql(sql_table_comment)

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
#             SQLite3Adapter.Column(
#                 name="post_content",
#                 data_type="TEXT",
#                 constraints=[C.NotNullConstraint("Post", "post_content")],
#             ),
#         ]

#         table = SQLite3Adapter.Table(name="Post", columns=columns)

#     m = MigrationElement()
#     m.migrate()

#     tables = SqliteInspector().get_tables()

#     assert len(tables) == 2
#     assert tables[0].name == "User"
#     assert tables[0].columns[0].name == "user_id"
#     assert tables[0].columns[0].data_type == "INTEGER"
#     assert tables[0].columns[0].constraints == [
#         C.PrimaryKeyConstraint("User", "user_id")
#     ]
#     assert tables[0].columns[1].name == "user_name"
#     assert tables[0].columns[1].data_type == "TEXT"
#     assert tables[0].columns[1].constraints == [
#         C.NotNullConstraint("User", "user_name")
#     ]

#     assert tables[1].name == "Post"
#     assert tables[1].columns[0].name == "post_id"
#     assert tables[1].columns[0].data_type == "INTEGER"
#     assert tables[1].columns[0].constraints == [
#         C.PrimaryKeyConstraint("Post", "post_id")
#     ]
#     assert tables[1].columns[1].name == "post_name"
#     assert tables[1].columns[1].data_type == "TEXT"
#     assert tables[1].columns[1].constraints == [
#         C.NotNullConstraint("Post", "post_name")
#     ]
#     assert tables[1].columns[2].name == "post_content"
#     assert tables[1].columns[2].data_type == "TEXT"
#     assert tables[1].columns[2].constraints == [
#         C.NotNullConstraint("Post", "post_content")
#     ]
