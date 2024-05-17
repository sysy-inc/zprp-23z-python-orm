import importlib
from os import path
import sys
from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig


def db_config_dynamic_import(schema_file_path: str) -> BaseDbConfig:
    if not path.exists(schema_file_path):
        raise FileNotFoundError(f"Schema file {schema_file_path} not found")
    if not path.isfile(schema_file_path):
        raise TypeError(f"Schema file {schema_file_path} is not a file")
    file = path.basename(schema_file_path)
    dir = path.dirname(schema_file_path)
    sys.path.append(dir)
    importlib.import_module(file[:-3])

    return BaseDbConfig.get_instance()
