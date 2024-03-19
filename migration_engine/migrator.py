from adapters.sqlite3_adapter import SQLite3Adapter


class BaseTable:
    @classmethod
    def migrate(cls):
        table = BaseTable.__subclasses__()
        for cls in table:
            print(cls.__name__, cls.__dict__)
            cls()


class Table(BaseTable):
    def __init__(self):
        self.adapter = SQLite3Adapter()

        models = Table.__subclasses__()

        for cls in models:
            # get some info from class inheriting from Table (cls.__dict__, cls(), ...)
            # self.adapter.create_table(name, type_safe_data)
            print(cls.__name__, cls.__dict__)


class User(Table):
    name = "test_name"


class Post(Table):
    title = "test_title"


if __name__ == "__main__":
    BaseTable.migrate()
