import pytest

from skibidi_orm.migration_engine.adapters.sqlite3_typing import SQLite3Typing
from skibidi_orm.migration_engine.converters.sqlite3.tables import (
    SQLite3TableOperationConverter,
)
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    CheckConstraint,
    Constraint,
    ConstraintType,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    UniqueConstraint,
    NotNullConstraint,
)
from skibidi_orm.migration_engine.operations.table_operations import (
    CreateTableOperation,
    DeleteTableOperation,
    RenameTableOperation,
)
from itertools import chain

from skibidi_orm.migration_engine.revisions.constants import get_revision_table_name


simple_table_no_constraints = SQLite3Typing.Table(
    "users", columns=[SQLite3Typing.Column("name", "TEXT")]
)


complex_table_no_constraints = SQLite3Typing.Table(
    "users",
    columns=[
        SQLite3Typing.Column("name", "TEXT"),
        SQLite3Typing.Column("age", "INTEGER"),
        SQLite3Typing.Column("email", "TEXT"),
        SQLite3Typing.Column("active", "BLOB"),
    ],
)

complex_table_with_constraints = SQLite3Typing.Table(
    "admin_users",
    columns=[
        SQLite3Typing.Column(
            "user_id",
            "INTEGER",
            column_constraints=[
                PrimaryKeyConstraint("users", "user_id"),
                NotNullConstraint("users", "user_id"),
            ],
        ),
        SQLite3Typing.Column("name", "TEXT"),
        SQLite3Typing.Column(
            "email", "TEXT", column_constraints=[UniqueConstraint("users", "email")]
        ),
        SQLite3Typing.Column("active", "BLOB", column_constraints=list()),
        SQLite3Typing.Column(
            "age",
            "INTEGER",
        ),
    ],
    table_constraints=[
        ForeignKeyConstraint(
            "admin_users", "users", {"active": "active", "name": "name"}
        ),
        CheckConstraint("admin_users", "age > 18"),
    ],
)


def test_create_table_conversion_simple():
    """Create a simple table"""
    operation = CreateTableOperation(simple_table_no_constraints)
    assert (
        SQLite3TableOperationConverter.convert_table_operation_to_SQL(operation)
        == "CREATE TABLE users (name TEXT);"
    )


def test_create_table_conversion_complex():
    """Create a complex table"""
    operation = CreateTableOperation(complex_table_no_constraints)
    assert (
        SQLite3TableOperationConverter.convert_table_operation_to_SQL(operation)
        == "CREATE TABLE users (name TEXT, age INTEGER, email TEXT, active BLOB);"
    )


def test_create_table_conversion_complex_with_constraints():
    """Create a complex table with multiple constraints"""
    operation = CreateTableOperation(complex_table_with_constraints)
    assert (
        SQLite3TableOperationConverter.convert_table_operation_to_SQL(operation)
        == "CREATE TABLE admin_users (user_id INTEGER PRIMARY KEY NOT NULL, name TEXT, "
        "email TEXT UNIQUE, active BLOB, age INTEGER, FOREIGN KEY (active, name) REFERENCES users ("
        "active, name), CHECK (age > 18));"
    )


def test_delete_table_conversion():
    """Delete a simple table"""
    operation = DeleteTableOperation(simple_table_no_constraints)
    assert (
        SQLite3TableOperationConverter.convert_table_operation_to_SQL(operation)
        == "DROP TABLE users;"
    )


def test_rename_table_conversion_simple():
    """Rename a table"""
    operation = RenameTableOperation(simple_table_no_constraints, "users2")
    assert (
        SQLite3TableOperationConverter.convert_table_operation_to_SQL(operation)
        == "DROP TABLE users; CREATE TABLE users2 (name TEXT);"
    )


def test_correct_revision_table_SQL_conversion():
    """Tests whether the query used to create the internal revision table is correct"""
    assert SQLite3TableOperationConverter.get_revision_table_creation_query() == (
        f"CREATE TABLE {get_revision_table_name()} (rev REVISION NOT NULL);"
    )
