from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor
from skibidi_orm.migration_engine.converters.sqlite3.all import SQLite3Converter
from skibidi_orm.migration_engine.adapters.database_objects import constraints as c
from skibidi_orm.migration_engine.adapters.sqlite3_typing import SQLite3Typing
from skibidi_orm.migration_engine.operations import table_operations as TO
from skibidi_orm.migration_engine.operations import column_operations as CO

# Database: SQLite3
# Path: /home/maksym/studia/sem4/ZPRP/projekt/test_database.db


SQLite3Config("/home/maksym/studia/sem4/ZPRP/projekt/test_database.db")


# This is an auto-generated migration file.
# Executing this file will result in executing the proposed migration.


def migrate():

    # No operations to execute

    pass


if __name__ == "__main__":
    migrate()
