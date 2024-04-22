import sqlite3
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.sql_executor.base_sql_executor import BaseSQLExecutor


class SQLite3Executor(BaseSQLExecutor):

    @staticmethod
    def execute_sql(sql: str):
        sqlite_config = SQLite3Config.get_instance()
        with sqlite3.connect(sqlite_config.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
