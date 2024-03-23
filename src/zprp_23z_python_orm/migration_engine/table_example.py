# Example of how Table class and classes modeling DB schema can be implemented
from adapters.base_adapter import BaseAdapter
from adapters.sqlite3_adapter import SQLite3Adapter
from migration_element import MigrationElement


class Table(MigrationElement):
    """
    This is example of how Table class can be implemented
    Key notes, that have to be taken into account:
    - Table class HAVE to inherit from MigrationElement and MigrationElement MUST only have one class inheriting from it
    - Table class HAVE to have adapter attribute, which is instance of BaseAdapter or its child
    """

    adapter: BaseAdapter

    def __init__(self):
        self.adapter = SQLite3Adapter()

        # This will iterate over all classes that inherit from Table and create a table in the database
        models = Table.__subclasses__()

        # Creator of Table class can implement how to map their own class structure to fit the adapter

        # This will only populate the adapter in inside migration scripts, as Table will never be instantiated
        if self.__class__ == Table:
            for cls in models:
                table: SQLite3Adapter.Table
                data_type: SQLite3Adapter.DataTypes
                columns: list[SQLite3Adapter.Column] = []
                constraints: list[SQLite3Adapter.Constraints] = []

                if cls.__dict__["data_type"] == "my_definition_of_data_type":
                    data_type = "INTEGER"
                elif cls.__dict__["data_type"] == "my_other_definition":
                    data_type = "TEXT"
                elif cls.__dict__["data_type"] == "and_other":
                    data_type = "BLOB"

                constraints.append(cls.__dict__["constraints"])

                columns.append(
                    SQLite3Adapter.Column(
                        name=cls.__dict__["name"],
                        data_type=data_type,
                        constraints=constraints,
                    )
                )
                table = SQLite3Adapter.Table(name=cls.__name__, columns=columns)

                # Table, for each instance should properly inform the adapter about being created
                self.adapter.create_table(table)


class User(Table):
    name = "test_name"
    data_type = "my_definition_of_data_type"
    constraints = None
    data = []

    def insert_data(self, name, title):
        self.data.append((name, title))


class Post(Table):
    name = "test_title"
    data_type = "my_other_definition"
    constraints = None


class Comment(Table):
    name = "test_content"
    data_type = "and_other"
    constraints = None
