import pytest

from skibidi_orm.migration_engine.adapters.postgres_typing import PostgresTyping
from skibidi_orm.migration_engine.converters.postgres.tables import (
    PostgresTableOperationConverter,
)
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    CheckConstraint,
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


simple_table_no_constraints = PostgresTyping.Table(
    "users", columns=[PostgresTyping.Column("name", "TEXT")]
)


complex_table_no_constraints = PostgresTyping.Table(
    "users",
    columns=[
        PostgresTyping.Column("name", "TEXT"),
        PostgresTyping.Column("age", "INTEGER"),
        PostgresTyping.Column("email", "TEXT"),
        PostgresTyping.Column("active", "BYTEA"),
    ],
)

complex_table_with_constraints = PostgresTyping.Table(
    "admin_users",
    columns=[
        PostgresTyping.Column(
            "user_id",
            "INTEGER",
            column_constraints=[
                PrimaryKeyConstraint("users", "user_id"),
                NotNullConstraint("users", "user_id"),
            ],
        ),
        PostgresTyping.Column("name", "TEXT"),
        PostgresTyping.Column(
            "email", "TEXT", column_constraints=[UniqueConstraint("users", "email")]
        ),
        PostgresTyping.Column("active", "BYTEA", column_constraints=list()),
        PostgresTyping.Column(
            "age",
            "INTEGER",
            column_constraints=[CheckConstraint("users", "age", "> 18")],
        ),
    ],
    foreign_keys={
        ForeignKeyConstraint(
            "admin_users", "users", {"active": "active", "name": "name"}
        )
    },
)


@pytest.mark.parametrize(
    "operation, expected",
    [
        (
            CreateTableOperation(simple_table_no_constraints),
            "CREATE TABLE users (name TEXT);",
        ),
        (
            CreateTableOperation(complex_table_no_constraints),
            "CREATE TABLE users (name TEXT, age INTEGER, email TEXT, active BYTEA);",
        ),
        (
            CreateTableOperation(complex_table_with_constraints),
            "CREATE TABLE admin_users (user_id INTEGER PRIMARY KEY NOT NULL, name TEXT, "
            "email TEXT UNIQUE, active BYTEA, age INTEGER, CHECK (age > 18), FOREIGN KEY (active, name) REFERENCES users ("
            "active, name));",
        ),
        (
            DeleteTableOperation(simple_table_no_constraints),
            "DROP TABLE users;",
        ),
        (
            RenameTableOperation(simple_table_no_constraints, "users2"),
            "DROP TABLE users; CREATE TABLE users2 (name TEXT);",
        ),
    ],
)
def test_convert_table_operation_to_SQL(operation, expected):  # type: ignore
    """Test the conversion of a CreateTableOperation to SQL."""
    assert (
        PostgresTableOperationConverter.convert_table_operation_to_SQL(operation)  # type: ignore
        == expected
    )
