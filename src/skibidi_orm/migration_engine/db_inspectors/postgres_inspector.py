from __future__ import annotations

from typing import Any, cast

import skibidi_orm.migration_engine.adapters.database_objects.constraints as c
from skibidi_orm.migration_engine.adapters.postgres_typing import PostgresTyping
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

    def get_tables(self) -> list[PostgresTyping.Table]:
        return super().get_tables()

    def get_table_columns(self, table_name: str) -> list[PostgresTyping.Column]:
        """
        Get all columns from the table.
        """

        return [
            PostgresTyping.Column(
                name=column_name,
                data_type=self._get_column_data_type(table_name, column_name),
                column_constraints=self._get_column_constraints(
                    table_name, column_name
                ),
            )
            for column_name in self._get_table_columns_names(table_name)
        ]

    def _get_column_constraints(
        self, table_name: str, column_name: str
    ) -> list[c.ColumnSpecificConstraint]:
        """
        Get all column constraints from the table.
        """

        with self.config.connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT
                    tc.constraint_name,
                    tc.table_name,
                    tc.constraint_type,
                    c.column_name,
                    c.is_nullable
                FROM
                    information_schema.table_constraints AS tc
                JOIN
                    information_schema.constraint_column_usage AS ccu
                ON
                    tc.constraint_catalog = ccu.constraint_catalog
                    AND tc.constraint_schema = ccu.constraint_schema
                    AND tc.constraint_name = ccu.constraint_name
                JOIN
                    information_schema.columns AS c
                ON
                    c.table_catalog = ccu.table_catalog
                    AND c.table_schema = ccu.table_schema
                    AND c.table_name = ccu.table_name
                    AND c.column_name = ccu.column_name
                WHERE
                    tc.table_name = '{table_name}'
                    AND c.column_name = '{column_name}';
                """
            )

            constraints = cursor.fetchall()

        typed_results = [
            PostgresInformationSchemaColumnsRowSelected.from_tuple(constraint)
            for constraint in constraints
        ]

        res: list[c.ColumnSpecificConstraint] = []
        for result in typed_results:
            if result.is_nullable == "NO":
                res.append(c.NotNullConstraint(table_name, column_name))
            if result.constraint_type == "PRIMARY KEY":
                res.append(c.PrimaryKeyConstraint(table_name, column_name))
            if result.constraint_type == "UNIQUE":
                res.append(c.UniqueConstraint(table_name, column_name))

        return res

    def _get_table_columns_names(self, table_name: str) -> list[str]:
        """
        Get all columns names from the table.
        """

        with self.config.connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                """
            )

            columns = cursor.fetchall()

        return [column[0] for column in columns]

    def _get_column_data_type(
        self, table_name: str, column_name: str
    ) -> PostgresTyping.DataTypes:
        """
        Get the data type of the column.
        """
        with self.config.connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT data_type
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                AND column_name = '{column_name}'
                """
            )

            data_type = cursor.fetchone()
            if not data_type:
                raise ValueError(
                    f"Column '{column_name}' does not exist in table '{table_name}'"
                )

        data_type_upper = cast(str, data_type[0]).upper()
        return cast(PostgresTyping.DataTypes, data_type_upper)

    def _is_column_nullable(self, table_name: str, column_name: str) -> bool:
        """
        Check if the column is nullable.
        """

        with self.config.connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                AND column_name = '{column_name}'
                """
            )

            is_nullable = cursor.fetchone()
            if not is_nullable:
                raise ValueError(
                    f"Column '{column_name}' does not exist in table '{table_name}'"
                )

        return is_nullable[0] == "YES"

    def __holds_instance(self, array: list[Any], class_type: Any) -> bool:
        """
        Helper function to check if the array holds the instance of a class.
        """
        return any(isinstance(x, class_type) for x in array)
