from __future__ import annotations
from skibidi_orm.migration_engine.adapters.base_adapter import BaseAdapter
from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)
from skibidi_orm.migration_engine.adapters.sqlite3_typing import (
    SQLite3Typing,
)
from skibidi_orm.migration_engine.db_inspectors.sqlite.sqlite3_inspector import (
    SQLite3Inspector,
)
from skibidi_orm.migration_engine.state_manager.state_manager import StateManager

from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor


class SQLite3Adapter(BaseAdapter):
    """
    This is an adapter that will select the proper functionality of the whole migration engine to accommodate a SQLite3 database.
    """

    tables: list[SQLite3Typing.Table]

    def __init__(self) -> None:
        self.tables = []

    def create_table(self, table: SQLite3Typing.Table):
        """Informs the adapter about Table creation."""

        self.tables.append(table)

    def execute_migration(self, preview: bool = False):
        """Execute the migration process on a full adapter."""

        self.inspector = SQLite3Inspector()

        db_tables = self.inspector.get_tables()

        state_manager = StateManager[SQLite3Typing.Table](
            db_tables=db_tables,
            schema_tables=self.tables,
        )

        MigrationElement.operations = (
            state_manager.get_operations_transforming_database_schema_into_class_hierarchy_schema()
        )

        if not preview:
            SQLite3Executor.execute_operations(MigrationElement.operations)
