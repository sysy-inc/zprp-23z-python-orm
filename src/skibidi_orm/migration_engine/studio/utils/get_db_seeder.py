from skibidi_orm.migration_engine.data_mutator.base_data_mutator import BaseDataMutator
from skibidi_orm.migration_engine.data_mutator.sqlite3_data_mutatorr import (
    SQLite3DataMutator,
)
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import (
    SQLite3Inspector,
)


def get_db_mutator(db_inspector: BaseDbInspector) -> BaseDataMutator:
    if isinstance(db_inspector, SQLite3Inspector):
        return SQLite3DataMutator()
    raise NotImplementedError
