# Example of how Table class and classes modeling DB schema can be implemented
from adapters.base_adapter import BaseAdapter
from adapters.sqlite3_adapter import SQLite3Adapter
from base_table import BaseTable


class Table(BaseTable):
    """
    This is example of how Table class can be implemented
    Key notes, that have to be taken into account:
    - Table class HAVE to inherit from BaseTable and BaseTable MUST only have one class inheriting from it
    - Table class HAVE to have adapter attribute, which is instance of BaseAdapter or its child
    """

    adapter: BaseAdapter

    def __init__(self):
        self.adapter = SQLite3Adapter()

        models = Table.__subclasses__()

        for cls in models:
            # get some info from class inheriting from Table (cls.__dict__, cls(), ...)
            # self.adapter.create_table(name, type_safe_data)
            print(cls.__name__, cls.__dict__)
            self.adapter.create_table(
                cls.__name__,
                [
                    {
                        "name": "dummy_id",
                        "data_type": "INTEGER",
                        "constraints": "PRIMARY KEY",
                    }
                ],
            )


class User(Table):
    name = "test_name"


class Post(Table):
    title = "test_title"
