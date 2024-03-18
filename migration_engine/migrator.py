from dataclasses import dataclass
import inspect
from typing import Generic, Literal, TypeVar, TypedDict

from migration_engine.adapters.base_adapter import BaseAdapter
from migration_engine.adapters.sqlite3_adapter import SQLite3Adapter


# class Migrator:
#     _instance = None

#     def __init__(self):
#         self.metadata = {}

#     @staticmethod
#     def get_instance():
#         if Migrator._instance is None:
#             Migrator._instance = Migrator()
#         return Migrator._instance

#     def __execute(self, data):
#         print(data)
#         pass

#     def get_data(self):
#         t = Migrator.__subclasses__()

#         for cls in t:
#             print(cls)
#             print(cls.__dict__)
#             t_base = cls()

#     def create_relation(self, data):
#         self.metadata["chuj"] = data

#     def create_table(self, data):
#         pass


# ######
# migrator = Migrator.get_instance()
# migrator.get_data()
# print(migrator.metadata)


# class SingletonMeta(type):
#     """
#     The Singleton class can be implemented in different ways in Python. Some
#     possible methods include: base class, decorator, metaclass. We will use the
#     metaclass because it is best suited for this purpose.
#     """

#     _instances = {}

#     def __call__(cls, *args, **kwargs):
#         """
#         Possible changes to the value of the `__init__` argument do not affect
#         the returned instance.
#         """
#         if cls not in cls._instances:
#             instance = super().__call__(*args, **kwargs)
#             cls._instances[cls] = instance
#         return cls._instances[cls]


# class MigratorSingleton[T](metaclass=SingletonMeta):
#     def __init__(self, adapter: T):
#         print("init")
#         self.adapter = adapter

#     def set_column(self, name: str, data_type: T, constraints: T):
#         # self.adapter.
#         pass

#     def create_table(self, table_name: str, columns):
#         pass


class BaseTable:
    pass


class Migrator[T]:
    def __init__(self, adapter: T) -> None:
        if not isinstance(adapter, BaseAdapter):
            raise ValueError("Adapter must be a subclass of BaseAdapter")
        self.adapter = adapter
        pass

    def get_data(self):
        table = BaseTable.__subclasses__()

        for cls in table:
            print(cls)
            print(cls.__dict__)
            cls()


m = Migrator(2)


class Table(BaseTable):
    def __init__(self):
        # self.migrator = MigratorSingleton(PGAdapter())
        # self.column = ColumnCreator(PGAdapter())

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
        pass


class User(Table):
    name = "test_name"


class Post(Table):
    title = "test_title"


if __name__ == "__main__":
    pass
