from skibidi_orm.migration_engine.adapters.base_adapter import BaseAdapter
from typing import Any


# All classes need to inherit from this class if they participate in a migration
class MigrationElement:
    adapter: BaseAdapter
    operations: list[Any] = []

    #   @classmethod
    # todo: why is classmethod commented?
    def migrate(self, preview: bool = False):
        table = MigrationElement.__subclasses__()

        for cls in table:
            table_instance = cls()
            table_instance.adapter.execute_migration(preview)
            MigrationElement.operations = table_instance.adapter.operation_list
