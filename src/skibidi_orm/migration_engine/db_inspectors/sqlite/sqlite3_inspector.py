from typing import cast
from skibidi_orm.migration_engine.db_inspectors.sqlite.supporting_objects import (
    PragmaIndexInfoEntry,
    PragmaIndexListEntry,
    PragmaTableInfoEntry,
    PragmaForeignKeyListEntry,
)
import sqlite3
import re

from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector
from skibidi_orm.migration_engine.adapters.sqlite3_typing import (
    SQLite3Typing,
)
import skibidi_orm.migration_engine.adapters.database_objects.constraints as c
from skibidi_orm.migration_engine.revisions.constants import get_revision_table_name

type SQLite3PragmaForeignKeyList = list[PragmaForeignKeyListEntry]


class SQLite3Inspector(BaseDbInspector):
    """
    Used to get data from live SQLite3 database.
    Should only be instantiated when SQLite3 is choosen as the database.
    """

    def __init__(self) -> None:
        self.config = SQLite3Config.get_instance()

    def get_tables(
        self,
    ) -> list[SQLite3Typing.Table]:
        """
        Retrieve all tables from the database.
        """

        tables: list[SQLite3Typing.Table] = []
        tables_names = self.get_tables_names()
        foreign_keys = self.get_foreign_key_constraints()
        for table_name in tables_names:
            table_columns = self.get_table_columns(table_name)
            related_fks = {fk for fk in foreign_keys if fk.table_name == table_name}
            tables.append(
                SQLite3Typing.Table(
                    name=table_name,
                    columns=table_columns,
                    table_constraints=cast(set[c.TableWideConstraint], related_fks),
                )
            )

        return tables

    def get_tables_names(self) -> list[str]:
        """
        Retrieve just tables names from the database.
        """

        tables = self._sqlite_execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        return [
            name for table in tables if (name := table[0]) != get_revision_table_name()
        ]

    @staticmethod
    def foreign_keys_from_pragma_entries(
        table_entry_mapping: dict[str, list[PragmaForeignKeyListEntry]]
    ) -> set[c.ForeignKeyConstraint]:
        """Creates all of the ForeignKeyConstraint objects based on the entries
        gathered from the pragma table"""

        return_value: set[c.ForeignKeyConstraint] = set()

        for table_name, pragma_entry_list in table_entry_mapping.items():
            for id in set(entry.id for entry in pragma_entry_list):
                # todo: maybe it would be quicker to create a dict id: list[Entry] first?

                corresponding_entries = [
                    entry for entry in pragma_entry_list if entry.id == id
                ]
                referenced_table = corresponding_entries[0].table

                corresponding_constraint = c.ForeignKeyConstraint(
                    table_name,
                    referenced_table,
                    {
                        entry.from_column: entry.to_column
                        for entry in corresponding_entries
                    },
                )
                return_value.add(corresponding_constraint)

        return return_value

    def get_index_details(
        self, index: PragmaIndexListEntry
    ) -> list[PragmaIndexInfoEntry]:
        """Get all details regarding a specific index"""
        raw_pragma_index_info = self._sqlite_execute(
            f"PRAGMA index_info({index.name});"
        )
        return [
            PragmaIndexInfoEntry.from_tuple(entry) for entry in raw_pragma_index_info
        ]

    def get_all_indices_and_details(
        self, table_name: str
    ) -> dict[PragmaIndexListEntry, list[PragmaIndexInfoEntry]]:
        """Get all indices regarding a specific table and their details."""

        raw_pragma_index_list = self._sqlite_execute(
            f"PRAGMA index_list({table_name});"
        )
        indices = [
            PragmaIndexListEntry.from_tuple(entry) for entry in raw_pragma_index_list
        ]
        details = [self.get_index_details(index) for index in indices]
        return {index: detail for index, detail in zip(indices, details)}

    def get_all_unique_non_composite_indices(
        self, table_name: str
    ) -> dict[PragmaIndexListEntry, PragmaIndexInfoEntry]:
        """Get all non-composite indices created by the UNIQUE keyword from a table
        as well as their info entry objects."""
        indices_with_details = self.get_all_indices_and_details(table_name)
        # filter out only the indices created by the UNIQUE keyword, skip primary keys and artificial indices
        return {
            index: details.pop()
            for index, details in indices_with_details.items()
            if index.creation_method == "u" and len(details) == 1
        }

    # todo: could refactor for this to only return column names instead
    def get_all_unique_constraints(self, table_name: str) -> list[c.UniqueConstraint]:
        """Get all unique constraints from a given table. This only detects the unique constraints
        based on non-composite indices explicitly created from the UNIQUE keyword."""
        valid_indices = self.get_all_unique_non_composite_indices(table_name)
        if not valid_indices:
            return []
        return [
            c.UniqueConstraint(table_name, cast(str, entry.column_name))
            # casting since indices created by UNIQUE can't contain null as the column name
            for entry in valid_indices.values()
        ]

    def _get_all_check_conditions(self, table_creation_sql: str) -> list[str]:
        """Get all check conditions from the table creation SQL."""
        pattern = re.compile(r"CHECK\s*\(", re.IGNORECASE)

        # Find all the positions of 'CHECK' statements
        check_positions = [
            match.start() for match in pattern.finditer(table_creation_sql)
        ]

        conditions: list[str] = []

        for pos in check_positions:
            # Start position of the constraint
            start = pos + len("CHECK(") + 1  # move past the opening parenthesis
            balance = 1
            end = start

            while balance > 0 and end < len(table_creation_sql):
                if table_creation_sql[end] == "(":
                    balance += 1
                elif table_creation_sql[end] == ")":
                    balance -= 1
                end += 1

            # Extracting the constraint without the outer parentheses
            end -= 1
            condition = table_creation_sql[start:end].strip()
            conditions.append(condition)

        return conditions

    def get_all_check_constraints(self, table_name: str) -> list[c.CheckConstraint]:
        """Get all check constraints from the database."""
        query = f"SELECT * from sqlite_master where tbl_name = '{table_name}' and type = 'table';"
        query_result = self._sqlite_execute(query).pop()

        sql = query_result[4]

        check_conditions = self._get_all_check_conditions(sql)
        return [c.CheckConstraint(table_name, content) for content in check_conditions]

    def get_foreign_key_constraints(self) -> set[c.ForeignKeyConstraint]:
        """Get all foreign key constraints from the database."""

        tables_names = self.get_tables_names()
        pragma_results: dict[str, list[PragmaForeignKeyListEntry]] = {
            # Map tables to their pragma entries
            table: [
                PragmaForeignKeyListEntry.from_tuple(entry) for entry in fetched_result
            ]
            for table, fetched_result in (
                (table, self._sqlite_execute(f"PRAGMA foreign_key_list({table})"))
                for table in tables_names
            )
            if fetched_result
        }
        pragma_results = pragma_results  # todo: remove

        constraints: set[c.ForeignKeyConstraint] = (
            SQLite3Inspector.foreign_keys_from_pragma_entries(pragma_results)
        )
        return constraints

    def get_column_constraints(
        self, table_name: str, entry: PragmaTableInfoEntry
    ) -> list[c.ColumnWideConstraint]:
        """Get all constraints for a column determined by the pragma table info entry.
        and a name of the table."""
        constraints: list[c.ColumnWideConstraint] = []
        column_name = entry.name
        if entry.pk:
            constraints.append(
                c.PrimaryKeyConstraint(table_name=table_name, column_name=column_name)
            )
        if entry.notnull:
            constraints.append(
                c.NotNullConstraint(table_name=table_name, column_name=column_name)
            )
        if entry.dflt_value is not None:
            constraints.append(
                c.DefaultConstraint(
                    table_name=table_name,
                    column_name=column_name,
                    value=entry.dflt_value,
                )
            )
        unique_constraints_for_table = self.get_all_unique_constraints(table_name)
        constraints.extend(
            [c for c in unique_constraints_for_table if c.column_name == column_name]
        )
        return constraints

    def get_table_columns(self, table_name: str) -> list[SQLite3Typing.Column]:
        raw_pragma_table_info = self._sqlite_execute(
            f"PRAGMA table_info({table_name});"
        )
        pragma_entries = [
            PragmaTableInfoEntry.from_tuple(entry) for entry in raw_pragma_table_info
        ]
        """
        When given a table name, returns a list of Column objects inside it.
        """

        return [
            SQLite3Typing.Column(
                name=entry.name,
                data_type=cast(SQLite3Typing.DataTypes, entry.data_type),
                column_constraints=self.get_column_constraints(table_name, entry),
            )
            for entry in pragma_entries
        ]

    def _sqlite_execute(self, query: str):
        """
        Execute a query in the SQLite3 database, returns its result.
        """

        db_path = self.config.db_path
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            cursor.close()
        return data
