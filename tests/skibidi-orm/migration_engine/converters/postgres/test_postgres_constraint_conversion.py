from pytest import raises
import pytest
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


@pytest.mark.parametrize(
    "constraint, expected",
    [
        (PrimaryKeyConstraint("users", "id"), "PRIMARY KEY"),
        (UniqueConstraint("users", "email"), "UNIQUE"),
        (NotNullConstraint("users", "email"), "NOT NULL"),
        (
            ForeignKeyConstraint("users", "addresses", {"address_id": "id"}),
            "FOREIGN KEY (address_id) REFERENCES addresses (id)",
        ),
        (
            ForeignKeyConstraint(
                "admins",
                "users",
                {"user_id": "id", "address": "address", "group_id": "group"},
            ),
            "FOREIGN KEY (user_id, address, group_id) REFERENCES users (id, address, group)",
        ),
        (CheckConstraint("users", "age > 18"), "CHECK (age > 18)"),
    ],
)
def test_convert_constraint_to_SQL(constraint, expected):  # type: ignore
    """Test the conversion of various constraints to SQL."""
    assert SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint) == expected  # type: ignore


@pytest.mark.parametrize(
    "constraint, expected_error",
    [
        (DefaultConstraint("users", "name", "Gordon"), UnsupportedConstraintError),
    ],
)
def test_convert_constraint_to_SQL_error(constraint, expected_error):  # type: ignore
    """Test the conversion of a DefaultConstraint to SQL."""
    with raises(expected_error):  # type: ignore
        SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint)  # type: ignore
