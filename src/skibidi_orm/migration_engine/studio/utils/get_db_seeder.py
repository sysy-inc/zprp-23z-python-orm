from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector
from skibidi_orm.migration_engine.db_inspectors.sqlite3_inspector import SqliteInspector
from skibidi_orm.migration_engine.db_seeder.base_db_seeder import BaseDBSeeder
from skibidi_orm.migration_engine.db_seeder.sqlite3_db_seeder import SQLite3DBSeeder


def get_db_seeder(db_inspector: BaseDbInspector) -> BaseDBSeeder:
    if isinstance(db_inspector, SqliteInspector):
        return SQLite3DBSeeder()
    raise NotImplementedError
