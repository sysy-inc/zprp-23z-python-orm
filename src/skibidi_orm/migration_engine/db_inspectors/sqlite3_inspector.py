from __future__ import annotations
from typing import Any, Literal, cast
import sqlite3

from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector
from skibidi_orm.migration_engine.adapters.sqlite3_typing import SQLite3Typing
import skibidi_orm.migration_engine.operations.constraints as C

type SQLite3PragmaTableInfo = list[
    tuple[int, str, str, Literal[0, 1], Any, Literal[0, 1]]
]

type SQLite3PragmaForeignKeyListEntry = tuple[
    int,
    int,
    str,
    str,
    str,
    Literal["NO ACTION", "RESTRICT", "SET NULL", "SET DEFAULT", "CASCADE"],
    Literal["NO ACTION", "RESTRICT", "SET NULL", "SET DEFAULT", "CASCADE"],
    str,
]

type SQLite3PragmaForeignKeyList = list[SQLite3PragmaForeignKeyListEntry]


class SqliteInspector(BaseDbInspector):
    """
    Used to get data from live SQLite3 database.
    Should only be instantiated when SQLite3 is choosen as the database.
    """

    Table = SQLite3Typing.Table
    Relation = SQLite3Typing.Relation
    Column = SQLite3Typing.Column
    Constraints = SQLite3Typing.Constraints
    DataTypes = SQLite3Typing.DataTypes

    def __init__(self) -> None:
        self.config = SQLite3Config.get_instance()

    def get_tables(
        self,
    ) -> list[Table]:
        tables: list[SqliteInspector.Table] = []
        tables_names = self.get_tables_names()
        for table_name in tables_names:
            table_columns = self.get_table_columns(table_name)
            tables.append(SqliteInspector.Table(name=table_name, columns=table_columns))

        return tables

    def get_tables_names(self) -> list[str]:
        tables = self._sqlite_execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        return [table[0] for table in tables]

    def get_relations(self) -> list[Relation]:
        tables_names = self.get_tables_names()
        foreign_keys = {
            table: fetched_result
            for table, fetched_result in (
                (table, self._sqlite_execute(f"PRAGMA foreign_key_list({table})"))
                for table in tables_names
            )
            if fetched_result
        }

        relations: list[SqliteInspector.Relation] = [
            SqliteInspector.Relation(
                origin_column=origin_table_col_name,
                origin_table=origin_table_name,
                referenced_column=referenced_table_col_name,
                referenced_table=referenced_table,
            )
            for (origin_table_name, relation_list) in foreign_keys.items()
            for _, _, referenced_table, origin_table_col_name, referenced_table_col_name, _, _, _ in relation_list
        ]
        return relations

    def get_table_columns(self, table_name: str) -> list[Column]:
        columns: SQLite3PragmaTableInfo = self._sqlite_execute(
            f"PRAGMA table_info({table_name});"
        )

        return [
            SqliteInspector.Column(
                name=name,
                data_type=cast(SqliteInspector.DataTypes, data_type),
                constraints=[
                    cast(SqliteInspector.Constraints, constraint)
                    for constraint in [
                        (
                            C.PrimaryKeyConstraint(
                                table_name=table_name, column_name=name
                            )
                            if pk
                            else None
                        ),
                        (
                            C.NotNullConstraint(table_name=table_name, column_name=name)
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