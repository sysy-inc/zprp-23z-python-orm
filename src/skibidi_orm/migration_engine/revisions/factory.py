from typing import Any

from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable
from skibidi_orm.migration_engine.revisions.revision import Revision
from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig


class RevisionFactory:
    """Class responsible for creating revision objects
    when migrating"""

    def create_revision(
        self,
        config: BaseDbConfig,
        tables: list[BaseTable[Any]],
    ) -> Revision:
        """Creates a revision based on a table list and config object"""
        raise NotImplementedError()

    def create_schema_string(self, tables: list[BaseTable[Any]]) -> str:
        """Creates a human-readable schema representation based on
        all of the tables within it"""
        raise NotImplementedError()
