from skibidi_orm.migration_engine.converters.base.interfaces import SQLQueryConverter
from skibidi_orm.migration_engine.revisions.constants import get_revision_table_name


class SQLite3QueryConverter(SQLQueryConverter):
    """Class responsible for converting query objects to SQLite3 SQL strings"""

    @staticmethod
    def convert_get_revision_data_query() -> str:
        return f"SELECT rowid, * FROM {get_revision_table_name()};"
