from skibidi_orm.migration_engine.converters.sqlite3.all import SQLite3Converter
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.revisions.manager import RevisionManager
from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor


def test_find_revision_table_existing_sqlite(make_database: str):
    """Tests whether the revision table is found if it exists"""
    SQLite3Config(make_database)
    assert not RevisionManager.find_revision_table()


def test_create_and_find_revision_table_sqlite(make_database: str):
    """Tests whether the revision table is found if it does not exist"""
    SQLite3Config(make_database)
    creation_string = (
        SQLite3Converter.get_table_operation_converter().get_revision_table_creation_query()
    )
    SQLite3Executor.execute_sql(creation_string)
    assert RevisionManager.find_revision_table()
