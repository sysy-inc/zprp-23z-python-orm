# class User(Table):  # type: ignore
#     columns = [
#         SQLite3Adapter.Column(
#             name="user_id",
#             data_type="INTEGER",
#             constraints=[C.PrimaryKeyConstraint("User", "user_id")],
#         ),
#         SQLite3Adapter.Column(
#             name="user_name",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("User", "user_name")],
#         ),
#     ]

#     table = SQLite3Adapter.Table(name="User", columns=columns)


# class Post(Table):  # type: ignore
#     columns = [
#         SQLite3Adapter.Column(
#             name="post_id",
#             data_type="INTEGER",
#             constraints=[C.PrimaryKeyConstraint("Post", "post_id")],
#         ),
#         SQLite3Adapter.Column(
#             name="post_name",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("Post", "post_name")],
#         ),
#     ]

#     table = SQLite3Adapter.Table(name="Post", columns=columns)


# ### DODANIE TABELI

# class Comment(Table):  # type: ignore

#     columns = [
#         SQLite3Adapter.Column(
#             name="comment_id",
#             data_type="INTEGER",
#             constraints=[C.PrimaryKeyConstraint("Comment", "comment_id")],
#         ),
#         SQLite3Adapter.Column(
#             name="comment_name",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("Comment", "comment_name")],
#         ),
#     ]

#     table = SQLite3Adapter.Table(name="Comment", columns=columns)


# ### ZMIANA NAZWY

# class NewNamePost(Table):  # type: ignore
#     columns = [
#         SQLite3Adapter.Column(
#             name="post_id",
#             data_type="INTEGER",
#             constraints=[C.PrimaryKeyConstraint("NewNamePost", "post_id")],
#         ),
#         SQLite3Adapter.Column(
#             name="post_name",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("NewNamePost", "post_name")],
#         ),
#     ]

#     table = SQLite3Adapter.Table(name="NewNamePost", columns=columns)r.Table(name="NewNamePost", columns=columns)


# ### Dodanie kolumny

#         SQLite3Adapter.Column(
#             name="post_content",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("Post", "post_content")],
#         ),


# ### POWROT

# class User(Table):  # type: ignore
#     columns = [
#         SQLite3Adapter.Column(
#             name="user_id",
#             data_type="INTEGER",
#             constraints=[C.PrimaryKeyConstraint("User", "user_id")],
#         ),
#         SQLite3Adapter.Column(
#             name="user_name",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("User", "user_name")],
#         ),
#     ]

#     table = SQLite3Adapter.Table(name="User", columns=columns)


# class Post(Table):  # type: ignore
#     columns = [
#         SQLite3Adapter.Column(
#             name="post_id",
#             data_type="INTEGER",
#             constraints=[C.PrimaryKeyConstraint("Post", "post_id")],
#         ),
#         SQLite3Adapter.Column(
#             name="post_name",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("Post", "post_name")],
#         ),
#     ]

#     table = SQLite3Adapter.Table(name="Post", columns=columns)


# class Comment(Table):  # type: ignore

#     columns = [
#         SQLite3Adapter.Column(
#             name="comment_id",
#             data_type="INTEGER",
#             constraints=[C.PrimaryKeyConstraint("Comment", "comment_id")],
#         ),
#         SQLite3Adapter.Column(
#             name="comment_name",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("Comment", "comment_name")],
#         ),
#     ]

#     table = SQLite3Adapter.Table(name="Comment", columns=columns)


# ### USUNIECIE I DODANIE TABELI

# class User(Table):  # type: ignore
#     columns = [
#         SQLite3Adapter.Column(
#             name="user_id",
#             data_type="INTEGER",
#             constraints=[C.PrimaryKeyConstraint("User", "user_id")],
#         ),
#         SQLite3Adapter.Column(
#             name="user_name",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("User", "user_name")],
#         ),
#     ]

#     table = SQLite3Adapter.Table(name="User", columns=columns)

# class Post(Table):  # type: ignore
#     columns = [
#         SQLite3Adapter.Column(
#             name="post_id",
#             data_type="INTEGER",
#             constraints=[C.PrimaryKeyConstraint("Post", "post_id")],
#         ),
#         SQLite3Adapter.Column(
#             name="post_name",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("Post", "post_name")],
#         ),
#         SQLite3Adapter.Column(
#             name="post_content",
#             data_type="TEXT",
#             constraints=[C.NotNullConstraint("Post", "post_content")],
#         ),
#     ]

#     table = SQLite3Adapter.Table(name="Post", columns=columns)
