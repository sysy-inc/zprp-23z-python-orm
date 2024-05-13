import pytest
from skibidi_orm.migration_engine.converters.sqlite3_converter import (
    SQLite3Converter,
    SQLite3TableOperationConverter,
)
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.operations.constraints import (
    CheckConstraint,
    Constraint,
    ConstraintType,
    ForeignKeyConstraint,
    PrimaryKeyConstraint,
    UniqueConstraint,
)
from skibidi_orm.migration_engine.operations.table_operations import (
    CreateTableOperation,
    DeleteTableOperation,
    RenameTableOperation,
)
from itertools import chain


simple_table_no_constraints = SQLite3Adapter.Table(
    "users", columns=[SQLite3Adapter.Column("name", "TEXT")]
)


complex_table_no_constraints = SQLite3Adapter.Table(
    "users",
    columns=[
        SQLite3Adapter.Column("name", "TEXT"),
        SQLite3Adapter.Column("age", "INTEGER"),
        SQLite3Adapter.Column("email", "TEXT"),
        SQLite3Adapter.Column("active", "BLOB"),
    ],
)

complex_table_with_constraints = SQLite3Adapter.Table(
    "admin_users",
    columns=[
        SQLite3Adapter.Column(
            "user_id",
            "INTEGER",
            column_constraints=[PrimaryKeyConstraint("users", "user_id")],
        ),
        SQLite3Adapter.Column("name", "TEXT"),
        SQLite3Adapter.Column(
            "email", "TEXT", column_constraints=[UniqueConstraint("users", "email")]
        ),
        SQLite3Adapter.Column("active", "BLOB", column_constraints=list()),
        SQLite3Adapter.Column(
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


@pytest.fixture
def non_random_constraint_order(monkeypatch: pytest.MonkeyPatch):
    """Since the actual split_constraints method works on sets, so the
    order of constraints is not guaranteed, we have to mock it using lists"""

    def split_using_lists(
        table: SQLite3Adapter.Table,
    ) -> tuple[list[Constraint], list[Constraint]]:
        all_constraints = list(
            chain.from_iterable(column.column_constraints for column in table.columns)
        )

        constraints_at_end = list(
            filter(
                lambda c: c.constraint_type
                not in [ConstraintType.PRIMARY_KEY, ConstraintType.UNIQUE],
                all_constraints,
            )
        )

        constraints_at_columns = [
            constraint
            for constraint in all_constraints
            if constraint not in constraints_at_end
        ]

        return list(constraints_at_end), list(constraints_at_columns)

    monkeypatch.setattr(SQLite3Converter, "split_constraints", split_using_lists)


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


@pytest.mark.usefixtures("non_random_constraint_order")
def test_create_table_conversion_complex_with_constraints():
    """Create a complex table with multiple constraints"""
    operation = CreateTableOperation(complex_table_with_constraints)
    assert (
        SQLite3TableOperationConverter.convert_table_operation_to_SQL(operation)
        == "CREATE TABLE admin_users (user_id INTEGER PRIMARY KEY, name TEXT, "
        "email TEXT UNIQUE, active BLOB, age INTEGER, CHECK (age > 18), FOREIGN KEY (active, name) REFERENCES users (active, name));"
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
