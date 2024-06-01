from typing import Any

from psycopg2 import ProgrammingError
from skibidi_orm.migration_engine.data_mutator.base_data_mutator import (
    BaseDataMutator,
    DeleteRowPk,
    InsertRowColumn,
)
from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig


class PostgresDataMutator(BaseDataMutator):
    def insert_row(self, table_name: str, row: list[InsertRowColumn]) -> None:
        """Insert a row in the table."""
        raise NotImplementedError

    def delete_row(self, table_name: str, pks: list[DeleteRowPk]) -> None:
        """Delete a row in the table. Row identified by primary key subset."""
        raise NotImplementedError

    def raw_query(self, query: str) -> list[Any]:
        """Execute a raw sql query in the database."""
        config = PostgresConfig.get_instance()
        with config.connection.cursor() as cursor:
            cursor.execute(query)
            try:
                return cursor.fetchall()
            except ProgrammingError:
                return []

    def get_rows(self, table_name: str, limit: int = 100, offset: int = 0) -> list[Any]:
        """Get paginated rows from the table."""
        config = PostgresConfig.get_instance()
        with config.connection.cursor() as cursor:
            cursor.execute(f"SELECT * FROM {table_name} LIMIT {limit} OFFSET {offset}")
            return cursor.fetchall()
