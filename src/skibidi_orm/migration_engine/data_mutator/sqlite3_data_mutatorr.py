import sqlite3
from skibidi_orm.migration_engine.data_mutator.base_data_mutator import (
    BaseDataMutator,
    InsertRowColumn,
)
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config


class SQLite3DataMutator(BaseDataMutator):

    def __init__(self):
        self.config = SQLite3Config.get_instance()

    def insert_row(self, table_name: str, row: list[InsertRowColumn]):
        query = f"INSERT INTO {table_name} ({', '.join([col.name for col in row])}) VALUES ({', '.join(['?' for _ in row])})"
        values = [col.value for col in row]
        self._sqlite_execute(query, values)

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
