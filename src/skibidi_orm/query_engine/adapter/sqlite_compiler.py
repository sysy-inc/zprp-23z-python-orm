"""
Compiler for SQLite.

This module defines the SQLiteCompiler class, which extends the base SQLCompiler
to handle SQLite-specific SQL statement compilation.
"""
from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler


class SQLiteCompiler(SQLCompiler):
    """
    SQLite-specific SQL compiler.

    This class inherits from SQLCompiler and is designed to handle the
    specific syntax and requirements of SQLite databases.
    """
    pass
