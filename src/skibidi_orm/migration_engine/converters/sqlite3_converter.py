from skibidi_orm.exceptions.constraints import UnsupportedConstraintError
from skibidi_orm.migration_engine.converters.sql_converter import SQLConverter
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.operations.column_operations import ColumnOperation
from skibidi_orm.migration_engine.operations.constraints import (
    CheckConstraint,
    Constraint,
    ConstraintType,
    ForeignKeyConstraint,
)
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from skibidi_orm.migration_engine.operations.table_operations import (
    DeleteTableOperation,
    RenameTableOperation,
    TableOperation,
    CreateTableOperation,
)
from skibidi_orm.exceptions.operations import UnsupportedOperationError
from typing import cast
from itertools import chain


class SQLite3Converter(SQLConverter):
    """Class reponsible for converting operation and constraint
    objects to SQLite3 SQL strings"""

    @classmethod
    def convert_table_operation_to_SQL(cls, operation: TableOperation) -> str:
        """Convert a given table operation to a SQLite3 SQL string"""
        if operation.operation_type == OperationType.CREATE:
            return cls._convert_create_table_operation_to_SQL(
                cast(CreateTableOperation, operation)
            )
        elif operation.operation_type == OperationType.DELETE:
            return cls._convert_drop_table_operation_to_SQL(
                cast(DeleteTableOperation, operation)
            )
        elif operation.operation_type == OperationType.RENAME:
            return cls._convert_rename_table_operation_to_SQL(
                cast(RenameTableOperation, operation)
            )
        else:
            raise UnsupportedOperationError(
                "The given operation is not supported in SQLite3."
            )

    @classmethod
    def convert_column_operation_to_SQL(cls, operation: ColumnOperation) -> str:
        """Convert a given column operation to a SQLite3 SQL string"""
        return ""

    @classmethod
    def convert_constraint_to_SQL(cls, constraint: Constraint) -> str:
        """Convert a given constraint to a SQLite3 SQL string"""
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
            return f"CHECK ({cast(CheckConstraint, constraint).column_name} {cast(CheckConstraint, constraint).condition})"
        else:
            raise UnsupportedConstraintError(
                f"Constraints of type {constraint.constraint_type} are not supported by SQLite3"
            )

    @classmethod
    def _convert_create_table_operation_to_SQL(
        cls, operation: CreateTableOperation
    ) -> str:
        """Convert a given create table operation to a SQLite3 SQL string"""
        definition_string = f"CREATE TABLE {operation.table.name}"
        constraints_at_end, constraints_at_columns = cls.split_constraints(
            operation.table
        )
        # TODO: refactor
        column_listing = (
            # (name1 datatype1, name2 datatype2, ...)
            ", ".join(
                " ".join(
                    element
                    for element in (
                        f"{column.name} {column.data_type}",
                        ", ".join(
                            cls.convert_constraint_to_SQL(constraint)
                            for constraint in column.constraints
                            if constraint in constraints_at_columns
                        ),
                    )
                    if element
                )
                for column in operation.table.columns
            )
        )

        constraints_at_end = ", ".join(
            cls.convert_constraint_to_SQL(constraint)
            for constraint in constraints_at_end
        )
        return " ".join(
            element
            for element in (
                definition_string,
                f"({', '.join(string for string in (column_listing, constraints_at_end) if string)});",
            )
        )

    @classmethod
    def _convert_drop_table_operation_to_SQL(
        cls, operation: DeleteTableOperation
    ) -> str:
        """Convert a given drop table operation to a SQLite3 SQL string"""
        return f"DROP TABLE {operation.table.name};"

    @classmethod
    def _convert_rename_table_operation_to_SQL(
        cls, operation: RenameTableOperation
    ) -> str:
        """Convert a given rename table operation to a SQLite3 SQL string. Since SQLite3 does not
        support renaming a table directly, a new table with the same columns has to be instantiated after
        deleting the original one."""
        delete_op = DeleteTableOperation(operation.table)
        create_op = CreateTableOperation(
            SQLite3Adapter.Table(operation.new_name, operation.table.columns)
        )
        return (
            cls.convert_table_operation_to_SQL(delete_op)
            + " "
            + cls.convert_table_operation_to_SQL(create_op)
        )

    @staticmethod
    def split_constraints(
        table: SQLite3Adapter.Table,
    ) -> tuple[set[Constraint], set[Constraint]]:
        # TODO: better typing
        """Split the constraints of a table into those that have to be added at the end of the
        table definition and those that have to be added in the definitions of their resective columns
        """
        all_constraints = set(
            chain.from_iterable(column.constraints for column in table.columns)
        )

        """These constraints have to be added at the end of the table definition, not by the
        columns they correspond to"""
        constraints_at_end = set(
            filter(
                lambda c: c.constraint_type
                not in [ConstraintType.PRIMARY_KEY, ConstraintType.UNIQUE],
                all_constraints,
            )
        )

        # These constraints have to be added in the column definition
        constraints_at_columns = all_constraints - constraints_at_end

        return set(constraints_at_end), set(constraints_at_columns)

    @classmethod
    def convert_constraint_list_to_SQL(cls, constraints: list[Constraint]) -> str:
        """Convert a list of constraints to a SQLite3 SQL string"""
        return ", ".join(
            cls.convert_constraint_to_SQL(constraint) for constraint in constraints
        )
