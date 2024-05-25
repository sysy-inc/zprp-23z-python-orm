import sqlite3
from skibidi_orm.exceptions.db_mutator_exceptions import AmbigiousDeleteRowError
from skibidi_orm.migration_engine.data_mutator.base_data_mutator import (
    BaseDataMutator,
    DeleteRowPk,
    InsertRowColumn,
)
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config


class SQLite3DataMutator(BaseDataMutator):

    def __init__(self):
        self.config = SQLite3Config.get_instance()

    def insert_row(self, table_name: str, row: list[InsertRowColumn]):
        """Insert a row in the table."""
        query = f"INSERT INTO {table_name} ({', '.join([col.name for col in row])}) VALUES ({', '.join(['?' for _ in row])})"
        values = [col.value for col in row]
        self._sqlite_execute(query, values)

    def delete_row(self, table_name: str, pks: list[DeleteRowPk]):
        """Delete a row in the table. Row identified by primary key subset."""
        deleted_rows = self._pre_select_to_delete_rows(table_name, pks)
        if len(deleted_rows) > 1:
            raise AmbigiousDeleteRowError(
                f"More than one row found with primary key subset: {pks}"
            )
        query = f"DELETE FROM {table_name} WHERE {' AND '.join([f'{pk.name} = ?' for pk in pks])}"
        values = [pk.value for pk in pks]
        self._sqlite_execute(query, values)

    def _pre_select_to_delete_rows(self, table_name: str, pks: list[DeleteRowPk]):
        """Select rows to be deleted. Used to check if the deletion is ambigious."""
        query = f"SELECT * FROM {table_name} WHERE {' AND '.join([f'{pk.name} = ?' for pk in pks])}"
        values = [pk.value for pk in pks]
        return self._sqlite_execute(query, values)

    def _sqlite_execute(self, query: str, values: list[str]):
        """
        Execute a query in the SQLite3 database, rutrns its result.
        """

        db_path = self.config.db_path
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, values)
            conn.commit()
            data = cursor.fetchall()
            cursor.close()
        return data

    def raw_query(self, query: str):
        """Execute a raw sql query in the database."""
        return self._sqlite_execute(query, [])

    def get_rows(self, table_name: str, limit: int = 100, offset: int = 0):
        """Get paginated rows from the table."""
        query = f"SELECT * FROM {table_name} LIMIT {limit} OFFSET {offset}"
        return self._sqlite_execute(query, [])
