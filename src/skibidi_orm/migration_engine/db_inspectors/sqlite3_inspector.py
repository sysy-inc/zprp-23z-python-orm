from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Literal, cast
import sqlite3

from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector
from skibidi_orm.migration_engine.adapters.database_objects.sqlite3_typing import (
    SQLite3Typing,
)
import skibidi_orm.migration_engine.adapters.database_objects.constraints as c

type SQLite3PragmaTableInfo = list[
    tuple[int, str, str, Literal[0, 1], Any, Literal[0, 1]]
]


@dataclass(frozen=True)
class PragmaForeignKeyListEntry:
    id: int
    seq: int
    table: str
    from_column: str
    to_column: str
    on_update: str
    on_delete: str
    match: str

    @classmethod
    def from_tuple(
        cls,
        values: tuple[str, str, str, str, str, str, str, str],
        # todo: better typing?
    ) -> PragmaForeignKeyListEntry:
        id, seq, table, from_column, to_column, on_update, on_delete, match = values
        return cls(
            int(id),
            int(seq),
            table,
            from_column,
            to_column,
            on_update,
            on_delete,
            match,
        )


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
        tables: list[SQLite3Typing.Table] = []
        tables_names = self.get_tables_names()
        for table_name in tables_names:
            table_columns = self.get_table_columns(table_name)
            tables.append(SQLite3Typing.Table(name=table_name, columns=table_columns))

        return tables

    def get_tables_names(self) -> list[str]:
        tables = self._sqlite_execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        return [table[0] for table in tables]

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

    def get_table_columns(self, table_name: str) -> list[SQLite3Typing.Column]:
        columns: SQLite3PragmaTableInfo = self._sqlite_execute(
            f"PRAGMA table_info({table_name});"
        )

        return [
            SQLite3Typing.Column(
                name=name,
                data_type=cast(SQLite3Typing.DataTypes, data_type),
                column_constraints=[
                    cast(c.ColumnSpecificConstraint, constraint)
                    for constraint in [
                        (
                            c.PrimaryKeyConstraint(
                                table_name=table_name, column_name=name
                            )
                            if pk
                            else None
                        ),
                        (
                            c.NotNullConstraint(table_name=table_name, column_name=name)
                            if notnull
                            else None
                        ),
                    ]
                    if constraint is not None
                ],
            )
            for _, name, data_type, notnull, _, pk in columns
        ]

    def _sqlite_execute(self, query: str):
        """
        Execute a query in the SQLite3 database, rutrns its result.
        """

        db_path = self.config.db_path
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            data = cursor.fetchall()
            cursor.close()
        return data
