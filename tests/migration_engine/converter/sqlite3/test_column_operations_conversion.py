from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.converters.sqlite3_converter import SQLite3Converter
from skibidi_orm.migration_engine.operations.column_operations import (
    AddColumnOperation,
    ChangeDataTypeOperation,
    DeleteColumnOperation,
    RenameColumnOperation,
)
from skibidi_orm.migration_engine.operations.constraints import (
    CheckConstraint,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    UniqueConstraint,
)


simple_column_no_constraints = SQLite3Adapter.Column("name", "TEXT")
column_primary_key_unique = SQLite3Adapter.Column(
    "user_id",
    "INTEGER",
    constraints=[
        PrimaryKeyConstraint("users", "user_id"),
        UniqueConstraint("users", "user_id"),
    ],
)

column_foreign_key_unique = SQLite3Adapter.Column(
    "user_id",
    "INTEGER",
    constraints=[
        ForeignKeyConstraint("users", "people", {"user_id": "person_id"}),
        UniqueConstraint("users", "user_id"),
    ],
)

column_check_constraint = SQLite3Adapter.Column(
    "age",
    "INTEGER",
    constraints=[CheckConstraint("users", "age", "> 18")],
)

empty_users_table = SQLite3Adapter.Table("users", columns=[])


def test_simple_column_definition():
    assert (
        SQLite3Converter.convert_column_definition_to_SQL(
            simple_column_no_constraints, []
        )
        == "name TEXT"
    )


def test_column_definition_with_primary_key_and_unique():
    assert (
        SQLite3Converter.convert_column_definition_to_SQL(
            column_primary_key_unique, column_primary_key_unique.constraints
        )
        == "user_id INTEGER PRIMARY KEY UNIQUE"
    )


def test_column_definition_with_foreign_key_and_unique():
    assert (
        SQLite3Converter.convert_column_definition_to_SQL(
            column_foreign_key_unique, column_foreign_key_unique.constraints
        )
        == "user_id INTEGER REFERENCES people (person_id) UNIQUE"
    )


def test_column_definition_with_check_constraint():
    assert (
        SQLite3Converter.convert_column_definition_to_SQL(
            column_check_constraint, column_check_constraint.constraints
        )
        == "age INTEGER CHECK (age > 18)"
    )


def test_add_simple_column():
    operation = AddColumnOperation(empty_users_table, simple_column_no_constraints)
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users ADD COLUMN name TEXT;"
    )


def test_add_column_with_primary_key_and_unique():
    operation = AddColumnOperation(empty_users_table, column_primary_key_unique)
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users ADD COLUMN user_id INTEGER PRIMARY KEY UNIQUE;"
    )


def test_add_column_with_foreign_key_and_unique():
    operation = AddColumnOperation(empty_users_table, column_foreign_key_unique)
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users ADD COLUMN user_id INTEGER REFERENCES people (person_id) UNIQUE;"
    )


def test_add_column_with_check_constraint():
    operation = AddColumnOperation(empty_users_table, column_check_constraint)
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users ADD COLUMN age INTEGER CHECK (age > 18);"
    )


def test_drop_simple_column():
    operation = DeleteColumnOperation(empty_users_table, simple_column_no_constraints)
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN name;"
    )


def test_drop_column_with_primary_key_and_unique():
    operation = DeleteColumnOperation(empty_users_table, column_primary_key_unique)
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN user_id;"
    )


def test_drop_column_with_foreign_key_and_unique():
    operation = DeleteColumnOperation(empty_users_table, column_foreign_key_unique)
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN user_id;"
    )


def test_drop_column_with_check_constraint():
    operation = DeleteColumnOperation(empty_users_table, column_check_constraint)
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN age;"
    )


def test_rename_simple_column():
    operation = RenameColumnOperation(
        empty_users_table, simple_column_no_constraints, "name2"
    )
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users RENAME COLUMN name TO name2;"
    )


def test_rename_column_with_primary_key_and_unique():
    operation = RenameColumnOperation(
        empty_users_table, column_primary_key_unique, "user_id2"
    )
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users RENAME COLUMN user_id TO user_id2;"
    )


def test_rename_column_with_foreign_key_and_unique():
    operation = RenameColumnOperation(
        empty_users_table, column_foreign_key_unique, "user_id2"
    )
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users RENAME COLUMN user_id TO user_id2;"
    )


def test_rename_column_with_check_constraint():
    operation = RenameColumnOperation(
        empty_users_table, column_check_constraint, "age2"
    )
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users RENAME COLUMN age TO age2;"
    )


def test_change_data_type_simple_column():
    operation = ChangeDataTypeOperation(
        empty_users_table, simple_column_no_constraints, "INTEGER"
    )
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN name; ALTER TABLE users ADD COLUMN name INTEGER;"
    )


def test_change_data_type_column_with_primary_key_and_unique():
    operation = ChangeDataTypeOperation(
        empty_users_table, column_primary_key_unique, "TEXT"
    )
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN user_id; ALTER TABLE users ADD COLUMN user_id TEXT PRIMARY KEY UNIQUE;"
    )


def test_change_data_type_column_with_foreign_key_and_unique():
    operation = ChangeDataTypeOperation(
        empty_users_table, column_foreign_key_unique, "TEXT"
    )
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN user_id; ALTER TABLE users ADD COLUMN user_id TEXT REFERENCES people (person_id) UNIQUE;"
    )


def test_change_data_type_column_with_check_constraint():
    operation = ChangeDataTypeOperation(
        empty_users_table, column_check_constraint, "TEXT"
    )
    assert (
        SQLite3Converter.convert_column_operation_to_SQL(operation)
        == "ALTER TABLE users DROP COLUMN age; ALTER TABLE users ADD COLUMN age TEXT CHECK (age > 18);"
    )
