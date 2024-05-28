from pytest import raises
from skibidi_orm.exceptions.operations import UnsupportedOperationError
from skibidi_orm.migration_engine.adapters.database_objects.sqlite3_typing import SQLite3Typing
from skibidi_orm.migration_engine.converters.sqlite3.columns import SQLite3ColumnOperationConverter
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


simple_column_no_constraints = SQLite3Typing.Column("name", "TEXT")
column_primary_key_unique = SQLite3Typing.Column(
    "user_id",
    "INTEGER",
    column_constraints=[
        PrimaryKeyConstraint("users", "user_id"),
        UniqueConstraint("users", "user_id"),
        NotNullConstraint("users", "user_id"),
    ],
)

column_unique = SQLite3Typing.Column(
    "user_id",
    "INTEGER",
    column_constraints=[
        UniqueConstraint("users", "user_id"),
    ],
)

column_check_constraint = SQLite3Typing.Column(
    "age",
    "INTEGER",
    column_constraints=[CheckConstraint("users", "age", "> 18")],
)

empty_users_table = SQLite3Typing.Table("users", columns=[])


def test_simple_column_definition():
    assert (
        SQLite3ColumnOperationConverter.convert_column_definition_to_SQL(
            simple_column_no_constraints, list()
        )
        == "name TEXT"
    )


def test_column_definition_with_primary_key_unique_nn():
    assert (
        SQLite3ColumnOperationConverter.convert_column_definition_to_SQL(
            column_primary_key_unique, column_primary_key_unique.column_constraints
        )
        == "user_id INTEGER PRIMARY KEY UNIQUE NOT NULL"
    )


def test_column_definition_unique():
    assert (
        SQLite3ColumnOperationConverter.convert_column_definition_to_SQL(
            column_unique, column_unique.column_constraints
        )
        == "user_id INTEGER UNIQUE"
    )


def test_column_definition_with_check_constraint():
    assert (
        SQLite3ColumnOperationConverter.convert_column_definition_to_SQL(
            column_check_constraint, column_check_constraint.column_constraints
        )
        == "age INTEGER CHECK (age > 18)"
    )


def test_add_simple_column():
    operation = AddColumnOperation(empty_users_table, simple_column_no_constraints)
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users ADD COLUMN name TEXT;"
    )


def test_add_column_with_primary_key_and_unique():
    operation = AddColumnOperation(empty_users_table, column_primary_key_unique)
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users ADD COLUMN user_id INTEGER PRIMARY KEY UNIQUE NOT NULL;"
    )


def test_add_column_with_foreign_key_and_unique():
    operation = AddColumnOperation(
        empty_users_table,
        column_unique,
        related_foreign_key=ForeignKeyConstraint(
            empty_users_table.name, "people", {"user_id": "person_id"}
        ),
    )
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users ADD COLUMN user_id INTEGER UNIQUE REFERENCES people (person_id);"
    )


def test_add_column_with_check_constraint():
    operation = AddColumnOperation(empty_users_table, column_check_constraint)
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users ADD COLUMN age INTEGER CHECK (age > 18);"
    )


def test_drop_simple_column():
    operation = DeleteColumnOperation(empty_users_table, simple_column_no_constraints)
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN name;"
    )


def test_drop_column_with_primary_key_and_unique():
    operation = DeleteColumnOperation(empty_users_table, column_primary_key_unique)
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN user_id;"
    )


def test_drop_column_with_foreign_key_and_unique():
    operation = DeleteColumnOperation(empty_users_table, column_unique)
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN user_id;"
    )


def test_drop_column_with_check_constraint():
    operation = DeleteColumnOperation(empty_users_table, column_check_constraint)
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN age;"
    )


def test_rename_simple_column():
    operation = RenameColumnOperation(
        empty_users_table, simple_column_no_constraints, "name2"
    )
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users RENAME COLUMN name TO name2;"
    )


def test_rename_column_with_primary_key_and_unique():
    operation = RenameColumnOperation(
        empty_users_table, column_primary_key_unique, "user_id2"
    )
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users RENAME COLUMN user_id TO user_id2;"
    )


def test_rename_column_with_foreign_key_and_unique():
    operation = RenameColumnOperation(empty_users_table, column_unique, "user_id2")
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users RENAME COLUMN user_id TO user_id2;"
    )


def test_rename_column_with_check_constraint():
    operation = RenameColumnOperation(
        empty_users_table, column_check_constraint, "age2"
    )
    assert (
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users RENAME COLUMN age TO age2;"
    )


def test_change_data_type_simple_column():
    operation = ChangeDataTypeOperation(
        empty_users_table, simple_column_no_constraints, "INTEGER"
    )
    with raises(UnsupportedOperationError):
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)


def test_change_data_type_primary_key_unique_nn():
    operation = ChangeDataTypeOperation(
        empty_users_table, column_primary_key_unique, "TEXT"
    )
    with raises(UnsupportedOperationError):
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)


def test_change_data_type_column_with_foreign_key_and_unique():
    operation = ChangeDataTypeOperation(empty_users_table, column_unique, "TEXT")

    with raises(UnsupportedOperationError):
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)


def test_change_data_type_column_with_check_constraint():
    operation = ChangeDataTypeOperation(
        empty_users_table, column_check_constraint, "TEXT"
    )
    with raises(UnsupportedOperationError):
        SQLite3ColumnOperationConverter.convert_column_operation_to_SQL(operation)
