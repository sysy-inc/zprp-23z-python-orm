from dataclasses import dataclass
import inspect
from typing import Literal, TypedDict


class Migrator:
    _instance = None

    def __init__(self):
        self.metadata = {}

    @staticmethod
    def get_instance():
        if Migrator._instance is None:
            Migrator._instance = Migrator()
        return Migrator._instance

    def __execute(self, data):
        print(data)
        pass

    def get_data(self):
        t = Migrator.__subclasses__()

        for cls in t:
            print(cls)
            print(cls.__dict__)
            t_base = cls()

    def create_relation(self, data):
        self.metadata["chuj"] = data

    def create_table(self, data):
        pass


# class SQLiteAdapter:
#     def __init__(self):
#         pass

#     def a(self, data):
#         pass

#     def b(self, data):
#         pass

# class PGAdapter:
#     def __init__(self):
#         pass

#     def a(self, data):
#         pass

#     def b(self, data):
#         pass


# class Table(Migrator):
#     meta = []

#     def __init__(self):
#         # self.migrator =
#         t = Table.__subclasses__()

#         for cls in t:
#             print(cls.__dict__)
#             Migrator.get_instance().create_relation(cls.__dict__)


# class User(Table):
#     name = "Dupa"


# class Post(Table):
#     title = "chuj"


######
migrator = Migrator.get_instance()
migrator.get_data()
print(migrator.metadata)


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Adapter:
    data_types: str
    constraints: str
    pass


class SQLiteAdapter(Adapter):
    data_types: Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
    constraints: Literal["PRIMARY KEY", "UNIQUE", "NOT NULL", "DEFAULT"]

    def __init__(self):
        pass

    def a(self):
        pass

    def b(self):
        pass


class PGAdapter(Adapter):
    data_types: Literal["VARCHAR", "INTEGER", "REAL", "BLOB", "NULL"]
    constraints: Literal["PRIMARY KEY", "UNIQUE", "NOT NULL", "DEFAULT"]

    def __init__(self):
        pass

    def c(self):
        pass

    def d(self):
        pass


class ColumnCreator[T]:

    def __init__(self, adapter: T):
        self.adapter = adapter

    def create_column(self, name: str, data_type: T, constraints: T):
        pass


class MigratorSingleton[T](metaclass=SingletonMeta):
    def __init__(self, adapter: T):
        print("init")
        self.adapter = adapter

    def set_column(self, name: str, data_type: T, constraints: T):
        # self.adapter.
        pass


class Table(MigratorSingleton):
    def __init__(self):
        self.migrator = MigratorSingleton(PGAdapter())
        self.column = ColumnCreator(PGAdapter())

        # self.migrator.create_table(
        #     "testTable",
        #     [
        #         {
        #             "name": "id",
        #             "constraints": "PRIMARY KEY",
        #         }
        #     ],
        # )
        # t = Table.__subclasses__()

        # for cls in t:
        #     print(cls.__dict__)
        #     Migrator.get_instance().create_relation(cls.__dict__)

    def create_table(self, table_name: str, columns):
        pass


class User(Table):
    name = "Dupa"


class Post(Table):
    title = "chuj"


if __name__ == "__main__":
    pass
    # The client code.

    # if id(s1) == id(s2):
    #     print("Singleton works, both variables contain the same instance.")
    # else:
    #     print("Singleton failed, variables contain different instances.")
