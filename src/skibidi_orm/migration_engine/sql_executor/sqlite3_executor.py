import sqlite3
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.sql_executor.base_sql_executor import BaseSQLExecutor
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation
from skibidi_orm.migration_engine.operations.table_operations import TableOperation

from skibidi_orm.migration_engine.converters.sqlite3.all import SQLite3Converter


class SQLite3Executor(BaseSQLExecutor):

    @staticmethod
    def execute_sql(sql: str):
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
        for operation in operations:
            if isinstance(operation, TableOperation):
                SQLite3Executor.execute_sql(
                    SQLite3Converter.convert_table_operation_to_SQL(operation)
                )
            else:
                SQLite3Executor.execute_sql(
                    SQLite3Converter.convert_column_operation_to_SQL(operation)
                )
