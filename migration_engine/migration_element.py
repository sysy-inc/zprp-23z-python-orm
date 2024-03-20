from adapters.base_adapter import BaseAdapter


# All classes need to inherit from this class if they participate in a migration
class MigrationElement:
    adapter: BaseAdapter

    @classmethod
    def migrate(cls):
        table = MigrationElement.__subclasses__()
        for cls in table:
            # Do migration action
            # print(cls.__name__, cls.__dict__)
            table_instance = cls()
            table_instance.adapter.execute_migration()
