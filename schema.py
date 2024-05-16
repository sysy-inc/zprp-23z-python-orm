from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.adapters.database_objects import constraints as C
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config


class Table(MigrationElement):

    def __init__(self) -> None:
        self.adapter = SQLite3Adapter()

        models = Table.__subclasses__()
        if self.__class__ == Table:
            for cls in models:
                self.adapter.create_table(cls.__dict__["table"])


class Post(Table):  # type: ignore
    columns = [
        SQLite3Adapter.Column(
            name="post_id",
            data_type="INTEGER",
            constraints=[C.PrimaryKeyConstraint("Post", "post_id")],
        ),
        SQLite3Adapter.Column(
            name="post_name",
            data_type="TEXT",
            constraints=[C.NotNullConstraint("Post", "post_name")],
        ),
    ]

    table = SQLite3Adapter.Table(name="Post", columns=columns)


SQLite3Config("test_database.db")