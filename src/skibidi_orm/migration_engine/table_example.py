# Example of how Table class and classes modeling DB schema can be implemented
from skibidi_orm.migration_engine.adapters.base_adapter import BaseAdapter
from skibidi_orm.migration_engine.adapters.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
import skibidi_orm.migration_engine.adapters.database_objects.constraints as c
from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)


class Table(MigrationElement):
    """
    This is example of how Table class can be implemented
    Key notes, that have to be taken into account:
    - Table class HAVE to inherit from MigrationElement and MigrationElement MUST only have one class inheriting from it
    - Table class HAVE to have adapter attribute, which is instance of BaseAdapter or its child
    """

    adapter: BaseAdapter

    def __init__(self) -> None:
        self.adapter = SQLite3Adapter()

        # This will iterate over all classes that inherit from Table and create a table in the database
        models = Table.__subclasses__()

        # Creator of Table class can implement how to map their own class structure to fit the adapter

        # This will only populate the adapter in inside migration scripts, as Table will never be instantiated
        if self.__class__ == Table:
            for cls in models:
                table: SQLite3Typing.Table
                data_type: SQLite3Typing.DataTypes
                columns: list[SQLite3Typing.Column] = []
                all_constraints = cls.__dict__["constraints"]

                table_constraints: set[c.TableWideConstraint] = set(
                    constraint
                    for constraint in all_constraints
                    if isinstance(constraint, c.TableWideConstraint)
                )

                column_constraints = [
                    constraint
                    for constraint in all_constraints
                    if isinstance(constraint, c.ColumnWideConstraint)
                ]

                if cls.__dict__["data_type"] == "my_definition_of_data_type":
                    data_type = "INTEGER"
                elif cls.__dict__["data_type"] == "my_other_definition":
                    data_type = "TEXT"
                elif cls.__dict__["data_type"] == "and_other":
                    data_type = "BLOB"
                else:
                    data_type = "NULL"

                columns.append(
                    SQLite3Typing.Column(
                        name=cls.__dict__["name"],
                        data_type=data_type,
                        column_constraints=column_constraints,
                    )
                )
                table = SQLite3Typing.Table(
                    name=cls.__name__,
                    columns=columns,
                    table_constraints=table_constraints,
                )

                # Table, for each instance should properly inform the adapter about being created
                self.adapter.create_table(table)


class User(Table):
    name = "test_name"
    data_type = "my_definition_of_data_type"
    constraints = None
    data: list[tuple[str, str]] = []

    def insert_data(self, name: str, title: str):
        self.data.append((name, title))


class Post(Table):
    name = "test_title"
    data_type = "my_other_definition"
    constraints = None


class Comment(Table):
    name = "test_content"
    data_type = "and_other"
    constraints = None
