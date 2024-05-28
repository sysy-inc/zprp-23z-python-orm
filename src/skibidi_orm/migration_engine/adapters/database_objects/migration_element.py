from skibidi_orm.migration_engine.adapters.base_adapter import BaseAdapter

from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation
from skibidi_orm.migration_engine.operations.table_operations import TableOperation


# All classes need to inherit from this class if they participate in a migration
class MigrationElement:
    adapter: BaseAdapter
    operations: list[ColumnOperation | TableOperation] = []

    def migrate(self, preview: bool = False):
        table = MigrationElement.__subclasses__()

        for cls in table:
            table_instance = cls()
            table_instance.adapter.execute_migration(preview)
