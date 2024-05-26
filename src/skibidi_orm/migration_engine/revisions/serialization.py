from typing import Any
from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable
import pickle


def serialize_tables(tables: list[BaseTable[Any]]) -> bytes:
    """Serializes a list of all database tables so that they
    can be saved inside a blob column"""
    return pickle.dumps(tables)


def deserialize_tables(schema_data: bytes) -> list[BaseTable[Any]]:
    """Deserializes a list of tables from a pickled byte stream"""
    return pickle.loads(schema_data)
