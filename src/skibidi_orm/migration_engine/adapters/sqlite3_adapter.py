from __future__ import annotations

from skibidi_orm.migration_engine.adapters.base_adapter import BaseAdapter
from skibidi_orm.migration_engine.adapters.sqlite3_typing import SQLite3Typing
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import SqliteInspector

from skibidi_orm.migration_engine.schema_analysys.state_manager import StateManager

from skibidi_orm.migration_engine.operations.table_operations import TableOperation
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation


class SQLite3Adapter(BaseAdapter):

    DataTypes = SQLite3Typing.DataTypes
    Constraints = SQLite3Typing.Constraints
    Column = SQLite3Typing.Column
    Table = SQLite3Typing.Table
    Relation = SQLite3Typing.Relation
    Relation = Relation
    tables: list[Table] = []
    relations: list[Relation] = []

    def __init__(self):
        pass

    def create_table(self, table: Table):
        """Informs the adapter about Table creation."""

        self.tables.append(table)

    def create_relation(
        self,
        relation: Relation,
    ):
        """Informs the adapter about a relation creation."""

        self.relations.append(relation)
        print(
            f"Creating relation from {relation.origin_table}.{relation.origin_column} to {relation.referenced_table}.{relation.referenced_column}"
        )

    def execute_migration(self):
        """Execute the migration process on a full adapter."""

        self.inspector = SqliteInspector()

        db_tables = self.inspector.get_tables()
        db_relations = self.inspector.get_relations()

        state_manager = StateManager[self.Table](
            db_tables=db_tables,
            db_relations=db_relations,
            schema_tables=self.tables,
            schema_relations=self.relations,
        )

        self.operations = state_manager.get_operations()
