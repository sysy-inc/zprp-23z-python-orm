import sqlite3
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.sql_executor.base_sql_executor import BaseSQLExecutor
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation
from skibidi_orm.migration_engine.operations.table_operations import TableOperation

from skibidi_orm.migration_engine.converters.sqlite3.all import SQLite3Converter


class SQLite3Executor(BaseSQLExecutor):
    """
    Executes SQL statements and operations on a SQLite3 database.

    This class provides methods to execute SQL statements and operations on a SQLite3 database.
    It inherits from the BaseSQLExecutor class.

    Methods:
        execute_sql: Executes a single SQL statement.
        execute_operations: Executes a list of table or column operations.

    """

    @staticmethod
    def execute_sql(sql: str):
        """
        Executes a single SQL statement.

        Args:
            sql (str): The SQL statement to be executed.

        Returns:
            None

        """
        sqlite_config = SQLite3Config.get_instance()
        with sqlite3.connect(sqlite_config.db_path) as conn:
            cursor = conn.cursor()
            commands = sql.split(";")
            for command in commands:
                if not command:
                    continue
                cursor.execute(command.strip())
            conn.commit()

    @staticmethod
    def execute_operations(operations: list[TableOperation | ColumnOperation]):
        """
        Executes a list of table or column operations.

        Args:
            operations (list[TableOperation | ColumnOperation]): The list of table or column operations to be executed.

        Returns:
            None

        """
        for operation in operations:
            if isinstance(operation, TableOperation):
                SQLite3Executor.execute_sql(
                    SQLite3Converter.convert_table_operation_to_SQL(operation)
                )
            else:
                SQLite3Executor.execute_sql(
                    SQLite3Converter.convert_column_operation_to_SQL(operation)
                )
