from skibidi_orm.migration_engine.converters.base.interfaces import SQLQueryConverter
from skibidi_orm.migration_engine.revisions.constants import get_revision_table_name


class SQLite3QueryConverter(SQLQueryConverter):
    """Class responsible for converting query objects to SQLite3 SQL strings"""

    @staticmethod
    def get_revision_data_query() -> str:
        return f"SELECT rowid, * FROM {get_revision_table_name()};"

    @staticmethod
    def get_table_clearing_query() -> str:
        return f"""
            PRAGMA writable_schema = 1;
            DELETE FROM sqlite_master WHERE type IN ('table', 'index', 'trigger') AND name != '{get_revision_table_name()}';
            PRAGMA writable_schema = 0;
            COMMIT;
            VACUUM;
            PRAGMA INTEGRITY_CHECK;
            """
