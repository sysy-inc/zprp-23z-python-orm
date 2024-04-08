from typing import Any, Literal, cast
import sqlite3
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector


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

type SQLite3PragmaForeignKeyListWithTableName = tuple[
    SQLite3PragmaForeignKeyList,
    str,
]


class SqliteInspector(BaseDbInspector):
    """
    Used to get data from live SQLite3 database.
    Should only be instantiated when SQLite3 is choosen as the database.
    """

    def __init__(self) -> None:
        self.config = SQLite3Config.get_instance()

    def get_tables(
        self,
    ) -> list[SQLite3Adapter.Table]:
        tables: list[SQLite3Adapter.Table] = []
        tables_names = self.get_tables_names()
        for table_name in tables_names:
            table_columns = self.get_table_columns(table_name)
            tables.append(SQLite3Adapter.Table(name=table_name, columns=table_columns))

        return tables

    def get_tables_names(self) -> list[str]:
        tables = self._sqlite_execute(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )
        return [table[0] for table in tables]

    def get_relations(self) -> list[SQLite3Adapter.Relation]:
        tables_names = self.get_tables_names()
        foreign_keys: list[SQLite3PragmaForeignKeyListWithTableName] = list(
            filter(
                lambda x: x[0],
                [
                    (self._sqlite_execute(f"PRAGMA foreign_key_list({table})"), table)
                    for table in tables_names
                ],
            )
        )

        relations: list[SQLite3Adapter.Relation] = []
        for (
            relation_list,
            origin_table_name,
        ) in foreign_keys:
            for (
                _,
                _,
                referenced_table,
                origin_table_col_name,
                referenced_table_col_name,
                _,
                _,
                _,
            ) in relation_list:
                relations.append(
                    SQLite3Adapter.Relation(
                        origin_column=origin_table_col_name,
                        origin_table=origin_table_name,
                        referenced_column=referenced_table_col_name,
                        referenced_table=referenced_table,
                    )
                )

        return relations

    def get_table_columns(self, table_name: str) -> list[SQLite3Adapter.Column]:
        columns: SQLite3PragmaTableInfo = self._sqlite_execute(
            f"PRAGMA table_info({table_name});"
        )
        adapter_columns: list[SQLite3Adapter.Column] = []

        for _, name, data_type, notnull, _, pk in columns:
            constraints: list[SQLite3Adapter.Constraints] = []
            if pk:
                constraints.append("PRIMARY KEY")
            if notnull:
                constraints.append("NOT NULL")

            adapter_columns.append(
                SQLite3Adapter.Column(
                    name=name,
                    data_type=cast(SQLite3Adapter.DataTypes, data_type),
                    constraints=constraints,
                )
            )

        return adapter_columns

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
