from skibidi_orm.exceptions.constraints import UnsupportedConstraintError
from skibidi_orm.migration_engine.converters.base.interfaces import (
    ConstraintSQLConverter,
)
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    CheckConstraint,
    Constraint,
    ConstraintType,
    ForeignKeyConstraint,
)
from typing import cast


class PostgresConstraintConverter(ConstraintSQLConverter):
    """Class responsible for converting constraint objects to raw Postgres SQL strings"""

    @staticmethod
    def convert_constraint_change_operation_to_SQL(_: Constraint) -> str:
        """Convert a given constraint change operation to a Postgres SQL string"""
        raise NotImplementedError(
            "Constraint change operations are not supported in Postgres yet."
        )

    @staticmethod
    def convert_constraint_to_SQL(constraint: Constraint) -> str:
        """Convert a given constraint to a Postgres SQL string"""
        if constraint.constraint_type == ConstraintType.PRIMARY_KEY:
            return "PRIMARY KEY"
        elif constraint.constraint_type == ConstraintType.UNIQUE:
            return "UNIQUE"
        elif constraint.constraint_type == ConstraintType.FOREIGN_KEY:
            constraint = cast(ForeignKeyConstraint, constraint)
            return (
                f"FOREIGN KEY ({', '.join(constraint.column_mapping.keys())}) REFERENCES"
                f" {constraint.referenced_table} ({', '.join(constraint.column_mapping.values())})"
            )
        elif constraint.constraint_type == ConstraintType.CHECK:
            return f"CHECK ({cast(CheckConstraint, constraint).condition})"
        elif constraint.constraint_type == ConstraintType.NOT_NULL:
            return "NOT NULL"
        else:
            raise UnsupportedConstraintError(
                f"Constraints of type {constraint.constraint_type} are not supported by Postgres"
            )
