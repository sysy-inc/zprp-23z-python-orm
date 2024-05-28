from skibidi_orm.migration_engine.adapters.providers import DatabaseProvider
from skibidi_orm.migration_engine.converters.sqlite3.all import SQLite3Converter
from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig
from skibidi_orm.migration_engine.revisions.revision import Revision
from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor
import sqlite3


class RevisionManager:
    """Class responsible for moving between revisions"""

    def __init__(self):
        config_instance = BaseDbConfig.get_instance()
        database_provider = config_instance.database_provider

        if database_provider == DatabaseProvider.SQLITE3:
            self.converter = SQLite3Converter
            self.executor = SQLite3Executor
        # todo : get all revisions and store them in a list
        ...

    def find_revision_table(self) -> bool:
        """Used to find the revision table with the name
        specified by the user. Returns True if found,
        False otherwise"""
        # todo: maybe do one query instead of two for finding and fetching data
        try:
            revision_data_query = (
                self.converter.get_query_converter().convert_get_revision_data_query()
            )
            self.executor.execute_sql(revision_data_query)
            return True
        except (
            sqlite3.OperationalError
        ):  # todo: change to a more general exception type or inherit
            return False

    def create_revision_table(self) -> None:
        """If the revision table is not found when migrating,
        this is called to create it"""
        self.executor.execute_sql(
            self.converter.get_table_operation_converter().get_revision_table_creation_query()
        )

    def save_revision(self, revision: Revision) -> None:
        """Saves a given revision to the revision database"""
        raise NotImplementedError()

    def get_all_revisions(self) -> list[Revision]:
        """Returns all revisions in the database"""
        raise NotImplementedError()

    def go_to_revision(self, revision_id: int) -> None:
        """Checkouts the user to a given revision.
        THIS SHOULD BE ONLY PERFORMED ON AN EMPTY TABLE!"""
        raise NotImplementedError()

    def get_revision_by_id(self, revision_id: int) -> None:
        """Returns a revision object by its id. If not found,
        throws an exception"""
        raise NotImplementedError()

    def get_revision_SQL(self, revision: Revision) -> str:
        """Returns the SQL string, the execution of which
        will result in checkouting the revision"""
        raise NotImplementedError()
