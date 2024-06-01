from pytest import raises
from skibidi_orm.exceptions.constraints import UnsupportedConstraintError
from skibidi_orm.migration_engine.converters.sqlite3.constraints import (
    SQLite3ConstraintConverter,
)
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    PrimaryKeyConstraint,
    UniqueConstraint,
    ForeignKeyConstraint,
    CheckConstraint,
    DefaultConstraint,
    NotNullConstraint,
)


def test_primary_key_constraint_conversion():
    """Test the conversion of a PrimaryKeyConstraint to SQL."""
    constraint = PrimaryKeyConstraint("users", "id")
    assert (
        SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint)
        == "PRIMARY KEY"
    )


def test_unique_constraint_conversion():
    """Test the conversion of a UniqueConstraint to SQL.""" ""
    constraint = UniqueConstraint("users", "email")
    assert SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint) == "UNIQUE"


def test_not_null_constraint_conversion():
    """Test the conversion of a NotNullConstraint to SQL."""
    constraint = NotNullConstraint("users", "email")
    assert (
        SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint) == "NOT NULL"
    )


def test_default_constraint_conversion():
    """Test the conversion of a DefaultConstraint to SQL."""
    with raises(UnsupportedConstraintError):
        SQLite3ConstraintConverter.convert_constraint_to_SQL(
            DefaultConstraint("users", "name", "Gordon")
        )


def test_single_column_foreign_key_constraint_conversion():
    """Test the conversion of a ForeignKeyConstraint with a single column to SQL."""
    constraint = ForeignKeyConstraint("users", "addresses", {"address_id": "id"})
    assert SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint) == (
        "FOREIGN KEY (address_id) REFERENCES addresses (id)"
    )


def test_composite_foreign_key_constraint_conversion():
    """Test the conversion of a ForeignKeyConstraint with multiple columns to SQL.""" ""
    constraint = ForeignKeyConstraint(
        "admins", "users", {"user_id": "id", "address": "address", "group_id": "group"}
    )
    assert (
        SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint)
        == "FOREIGN KEY (user_id, address, group_id) REFERENCES users (id, address, group)"
    )


def test_check_constraint_conversion():
    """Test the conversion of a CheckConstraint to SQL.""" ""
    constraint = CheckConstraint("users", "age > 18")
    assert (
        SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint)
        == "CHECK (age > 18)"
    )
