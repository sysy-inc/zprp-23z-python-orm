from __future__ import annotations
from skibidi_orm.migration_engine.adapters.base_adapter import BaseAdapter
from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)
from skibidi_orm.migration_engine.adapters.postgres_typing import PostgresTyping
from skibidi_orm.migration_engine.db_inspectors.postgres_inspector import (
    PostgresInspector,
)
from skibidi_orm.migration_engine.state_manager.state_manager import StateManager


class PostgresAdapter(BaseAdapter):

    tables: list[PostgresTyping.Table]

    def __init__(self) -> None:
        self.tables = []

    def create_table(self, table: PostgresTyping.Table):
        """Informs the adapter about Table creation."""

        self.tables.append(table)

    def execute_migration(self, preview: bool = False):
        """Execute the migration process on a full adapter."""

        self.inspector = PostgresInspector()

        db_tables = self.inspector.get_tables()

        state_manager = StateManager[PostgresTyping.Table](
            db_tables=db_tables,
            schema_tables=self.tables,
        )

        MigrationElement.operations = state_manager.get_operations()

        # if not preview:
        #     SQLite3Executor.execute_operations(MigrationElement.operations)
