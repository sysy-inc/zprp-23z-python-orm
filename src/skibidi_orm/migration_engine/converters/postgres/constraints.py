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
        if constraint.constraint_type == ConstraintType.PRIMARY_KEY:
            return "PRIMARY KEY"
        elif constraint.constraint_type == ConstraintType.UNIQUE:
            return "UNIQUE"
        elif constraint.constraint_type == ConstraintType.FOREIGN_KEY:
            constraint = cast(ForeignKeyConstraint, constraint)
            column_mappings = ", ".join(
                f"{col} REFERENCES {constraint.referenced_table}({ref_col})"
                for col, ref_col in constraint.column_mapping.items()
            )
            return f"FOREIGN KEY ({column_mappings})"
        elif constraint.constraint_type == ConstraintType.CHECK:
            return f"CHECK ({cast(CheckConstraint, constraint).column_name} {cast(CheckConstraint, constraint).condition})"
        elif constraint.constraint_type == ConstraintType.NOT_NULL:
            return "NOT NULL"
        else:
            raise UnsupportedConstraintError(
                f"Constraint type {constraint.constraint_type} is not supported."
            )
