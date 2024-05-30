from skibidi_orm.migration_engine.adapters.base_adapter import BaseAdapter

from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation
from skibidi_orm.migration_engine.operations.table_operations import TableOperation


# All classes need to inherit from this class if they participate in a migration
class MigrationElement:
    """
    Base class for all migration elements. Every class that wants to participate in a migration should inherit from this class.
    """

    adapter: BaseAdapter
    operations: list[ColumnOperation | TableOperation] = []

    def migrate(self, preview: bool = False):
        """
        This will execute the migration for all the migration elements.

        """
        table = MigrationElement.__subclasses__()

        for cls in table:
            table_instance = cls()
            table_instance.adapter.execute_migration(preview)
