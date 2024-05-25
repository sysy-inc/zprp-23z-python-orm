from typing import Any
from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable
from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig


def serialize_tables(tables: list[BaseTable[Any]]) -> bytes:
    """Serializes a list of all database tables so that they
    can be saved inside a blob column"""
    raise NotImplementedError()


def serialize_config(config: BaseDbConfig) -> bytes:
    """Serializes the database config used during a migration
    so that it can be saved inside a blob column"""
    raise NotImplementedError()


def deserialize_tables(data: bytes) -> list[BaseTable[Any]]:
    """Deserializes a list of tables from a pickled byte stream"""
    raise NotImplementedError()


def deserialize_config(data: bytes) -> BaseDbConfig:
    """Deserializes a database config object from a pickled byte stream"""
    raise NotImplementedError()
