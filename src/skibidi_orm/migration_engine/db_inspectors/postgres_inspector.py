from typing import Any
from skibidi_orm.migration_engine.adapters.base_adapter import BaseColumn, BaseTable
from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector


class PostgresInspector(BaseDbInspector):
    """
    Used to get data from live Postgres database.
    Should only be instantiated when Postgres is choosen as the database.
    """

    def __init__(self) -> None:
        self.config = PostgresConfig.get_instance()

    def get_tables_names(self) -> list[str]:
        """
        Get all tables names from the database.
        """

        with self.config.connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                """
            )

            tables = cursor.fetchall()

        return [table[0] for table in tables]

    def get_tables(self) -> list[BaseTable[BaseColumn[Any]]]:
        return super().get_tables()

    def get_table_columns(self, table_name: str) -> list[BaseColumn[Any]]:
        return super().get_table_columns(table_name)
