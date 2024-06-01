from pytest import raises
import pytest
from skibidi_orm.exceptions.operations import UnsupportedOperationError
from skibidi_orm.migration_engine.adapters.postgres_typing import PostgresTyping
from skibidi_orm.migration_engine.converters.postgres.columns import (
    PostgresColumnOperationConverter,
)
from skibidi_orm.migration_engine.operations.column_operations import (
    AddColumnOperation,
    ChangeDataTypeOperation,
    DeleteColumnOperation,
    RenameColumnOperation,
)
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    CheckConstraint,
    ForeignKeyConstraint,
    NotNullConstraint,
    PrimaryKeyConstraint,
    UniqueConstraint,
)

simple_column_no_constraints = PostgresTyping.Column("name", "TEXT")
column_primary_key_unique = PostgresTyping.Column(
    "user_id",
    "INTEGER",
    column_constraints=[
        PrimaryKeyConstraint("users", "user_id"),
        UniqueConstraint("users", "user_id"),
        NotNullConstraint("users", "user_id"),
    ],
)

column_unique = PostgresTyping.Column(
    "user_id",
    "INTEGER",
    column_constraints=[
        UniqueConstraint("users", "user_id"),
    ],
)

column_check_constraint = PostgresTyping.Column(
    "age",
    "INTEGER",
)

empty_users_table = PostgresTyping.Table("users", columns=[])


@pytest.mark.parametrize(
    "column, constraints_list, expected",
    [
        (simple_column_no_constraints, [], "name TEXT"),
        (
                column_primary_key_unique,
                column_primary_key_unique.column_constraints,
                "user_id INTEGER PRIMARY KEY UNIQUE NOT NULL",
        ),
        (
                column_unique,
                column_unique.column_constraints,
                "user_id INTEGER UNIQUE",
        ),
        (
                column_check_constraint,
                column_check_constraint.column_constraints,
                "age INTEGER",
        ),
    ],
)
def test_convert_column_definition_to_SQL(column, constraints_list, expected):  # type: ignore
    assert (
            PostgresColumnOperationConverter.convert_column_definition_to_SQL(
                column, constraints_list  # type: ignore
            )
            == expected
    )


@pytest.mark.parametrize(
    "operation, expected",
    [
        (
                AddColumnOperation(empty_users_table, simple_column_no_constraints),
                "ALTER TABLE users ADD COLUMN name TEXT;",
        ),
        (
                AddColumnOperation(empty_users_table, column_primary_key_unique),
                "ALTER TABLE users ADD COLUMN user_id INTEGER PRIMARY KEY UNIQUE NOT NULL;",
        ),
        (
                AddColumnOperation(
                    empty_users_table,
                    column_unique,
                    related_foreign_key=ForeignKeyConstraint(
                        empty_users_table.name, "people", {"user_id": "person_id"}
                    ),
                ),
                "ALTER TABLE users ADD COLUMN user_id INTEGER UNIQUE REFERENCES people (person_id);",
        ),
        (
                AddColumnOperation(empty_users_table, column_check_constraint,
                                   related_check_constraint=CheckConstraint("users", "age > 18")),
                "ALTER TABLE users ADD COLUMN age INTEGER CHECK (age > 18);",
        ),
        (
                DeleteColumnOperation(empty_users_table, simple_column_no_constraints),
                "ALTER TABLE users DROP COLUMN name;",
        ),
        (
                DeleteColumnOperation(empty_users_table, column_primary_key_unique),
                "ALTER TABLE users DROP COLUMN user_id;",
        ),
        (
                DeleteColumnOperation(empty_users_table, column_unique),
                "ALTER TABLE users DROP COLUMN user_id;",
        ),
        (
                DeleteColumnOperation(empty_users_table, column_check_constraint),
                "ALTER TABLE users DROP COLUMN age;",
        ),
        (
                RenameColumnOperation(
                    empty_users_table, simple_column_no_constraints, "name2"
                ),
                "ALTER TABLE users RENAME COLUMN name TO name2;",
        ),
        (
                RenameColumnOperation(
                    empty_users_table, column_primary_key_unique, "user_id2"
                ),
                "ALTER TABLE users RENAME COLUMN user_id TO user_id2;",
        ),
        (
                RenameColumnOperation(empty_users_table, column_unique, "user_id2"),
                "ALTER TABLE users RENAME COLUMN user_id TO user_id2;",
        ),
        (
                RenameColumnOperation(empty_users_table, column_check_constraint, "age2"),
                "ALTER TABLE users RENAME COLUMN age TO age2;",
        ),
    ],
)
def test_convert_column_operation_to_SQL(operation, expected):  # type: ignore
    assert (
            PostgresColumnOperationConverter.convert_column_operation_to_SQL(operation)  # type: ignore
            == expected
    )


@pytest.mark.parametrize(
    "operation, expected_error",
    [
        (
                ChangeDataTypeOperation(
                    empty_users_table, simple_column_no_constraints, "INTEGER"
                ),
                UnsupportedOperationError,
        ),
        (
                ChangeDataTypeOperation(
                    empty_users_table, column_primary_key_unique, "TEXT"
                ),
                UnsupportedOperationError,
        ),
        (
                ChangeDataTypeOperation(empty_users_table, column_unique, "TEXT"),
                UnsupportedOperationError,
        ),
        (
                ChangeDataTypeOperation(empty_users_table, column_check_constraint, "TEXT"),
                UnsupportedOperationError,
        ),
    ],
)
def test_convert_column_operation_to_SQL_errors(operation, expected_error):  # type: ignore
    with raises(expected_error):  # type: ignore
        PostgresColumnOperationConverter.convert_column_operation_to_SQL(operation)  # type: ignore
