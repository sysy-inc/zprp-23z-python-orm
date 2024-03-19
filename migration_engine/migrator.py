from adapters.base_adapter import BaseAdapter


class BaseTable:
    adapter: BaseAdapter

    @classmethod
    def migrate(cls):
        table = BaseTable.__subclasses__()
        for cls in table:
            print(cls.__name__, cls.__dict__)
            table_instance = cls()
            table_instance.adapter.execute_migration()


if __name__ == "__main__":
    BaseTable.migrate()
