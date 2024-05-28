from __future__ import annotations
from skibidi_orm.migration_engine.adapters.base_adapter import BaseAdapter
from skibidi_orm.migration_engine.adapters.database_objects.sqlite3_typing import SQLite3Typing
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import SQLite3Inspector
from skibidi_orm.migration_engine.state_manager.state_manager import StateManager

from skibidi_orm.migration_engine.operations.table_operations import TableOperation
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation

from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor


class SQLite3Adapter(BaseAdapter):

    tables: list[SQLite3Typing.Table] = []

    def __init__(self):
        self.reset_adapter()
        self.operations: list[TableOperation | ColumnOperation] = []

    @property
    def operation_list(self) -> list[TableOperation | ColumnOperation]:
        """Return the operation list"""

        return self.operations

    def create_table(self, table: SQLite3Typing.Table):
        """Informs the adapter about Table creation."""

        self.tables.append(table)

    def reset_adapter(self):
        """Reset the adapter"""
        self.tables = []

    def execute_migration(self, preview: bool = False):
        """Execute the migration process on a full adapter."""

        self.inspector = SQLite3Inspector()

        db_tables = self.inspector.get_tables()

        state_manager = StateManager[SQLite3Typing.Table](
            db_tables=db_tables,
            schema_tables=self.tables,
        )

        self.operations = state_manager.get_operations()
        if not preview:
            SQLite3Executor.execute_operations(self.operations)
