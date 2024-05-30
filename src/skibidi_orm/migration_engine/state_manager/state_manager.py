from skibidi_orm.migration_engine.adapters.base_adapter import (
    BaseTable,
    BaseColumn,
)
from typing import Any
from skibidi_orm.migration_engine.operations.column_operations import (
    ColumnOperation,
    AddColumnOperation,
    DeleteColumnOperation,
)

from skibidi_orm.migration_engine.operations.table_operations import (
    TableOperation,
    CreateTableOperation,
    DeleteTableOperation,
    RenameTableOperation,
)

from skibidi_orm.migration_engine.state_manager.i_state_manager import IStateManager


class StateManager[TTable: BaseTable[BaseColumn[Any]]](IStateManager):
    """
    Class that will analyze the differences between the database schema and the class structure defined schema
    when instantiated.

    It can provide a list of operations needed to transform the schema of the database to be equivalent with the
    one defined via python objects and migration files.
    """

    def __init__(
        self,
        db_tables: list[TTable],
        schema_tables: list[TTable],
    ) -> None:
        self.db_tables = db_tables
        self.schema_tables = schema_tables

        self.serviced_tables: list[TTable] = []

        self.operations: list[TableOperation | ColumnOperation] = []

        self._analyze_schemas()

    def _analyze_schemas(self):
        """
        Call helper functions to retrieve all operations needed for database transformation.
        """
        self._get_delete_tables_operations()
        self._get_create_tables_operations()
        self._get_delete_columns_operations()
        self._get_create_columns_operations()

    def get_operations_transforming_database_schema_into_class_hierarchy_schema(
        self,
    ) -> list[TableOperation | ColumnOperation]:
        """
        Return operations required for transforming the database calculated by the schema analysis.
        """
        return self.operations

    def _get_create_tables_operations(self) -> None:
        """
        Get operations concerning the creation of new tables.
        """

        t_db_names = set([t.name for t in self.db_tables])

        for s_table in self.schema_tables:
            if s_table.name not in t_db_names:
                if s_table not in self.serviced_tables:
                    self.operations.append(CreateTableOperation(s_table))
                    self.serviced_tables.append(s_table)

    def _get_delete_tables_operations(self) -> None:
        """
        Get operations concerning the deletion of tables.
        """

        class TableFound(Exception):
            pass

        t_schema_names = set([t.name for t in self.schema_tables])
        for db_table in self.db_tables:
            try:
                if db_table.name not in t_schema_names:
                    for s_table in self.schema_tables:
                        s_column_names = set([c.name for c in s_table.columns])
                        db_column_names = set([c.name for c in db_table.columns])

                        if s_column_names == db_column_names:
                            self.operations.append(
                                RenameTableOperation(db_table, s_table.name)
                            )
                            self.serviced_tables.append(s_table)
                            raise TableFound
                    if db_table not in self.serviced_tables:
                        self.operations.append(DeleteTableOperation(db_table))
                        self.serviced_tables.append(db_table)
            except TableFound:
                pass

    def _get_create_columns_operations(self):
        """
        Get operations concerning the creation of new columns.
        """

        db_table_dict = {t.name: t for t in self.db_tables}
        schema_table_dict = {t.name: t for t in self.schema_tables}

        for s_table_name, s_table in schema_table_dict.items():
            if s_table not in self.serviced_tables:
                if s_table_name in db_table_dict.keys():

                    table_db_columns = db_table_dict[s_table_name].columns
                    table_schema_columns = s_table.columns

                    for s_column in table_schema_columns:
                        if s_column not in table_db_columns:
                            self.operations.append(
                                AddColumnOperation(
                                    db_table_dict[s_table_name], s_column
                                )
                            )

    def _get_delete_columns_operations(self):
        """
        Get operations concerning the deletion of columns.
        """

        db_table_dict = {t.name: t for t in self.db_tables}
        schema_table_dict = {t.name: t for t in self.schema_tables}

        for db_table_name, db_table in db_table_dict.items():
            if db_table not in self.serviced_tables:
                if db_table_name in schema_table_dict.keys():

                    table_db_columns = db_table.columns
                    table_schema_columns = schema_table_dict[db_table_name].columns

                    for db_column in table_db_columns:
                        if db_column not in table_schema_columns:
                            self.operations.append(
                                DeleteColumnOperation(db_table, db_column)
                            )

    # def get_relations_operations(self):
    #     # TODO: implement using foreign keys
    #     for relation in self.schema_relations:
    #         if relation not in self.db_relations:
    #             pass
