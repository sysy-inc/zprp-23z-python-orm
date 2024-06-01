from skibidi_orm.migration_engine.adapters.sqlite3_typing import SQLite3Typing
from skibidi_orm.migration_engine.converters.base.interfaces import (
    ColumnOperationSQLConverter,
)
from skibidi_orm.migration_engine.converters.sqlite3.constraints import (
    SQLite3ConstraintConverter,
)
from skibidi_orm.migration_engine.operations.column_operations import (
    AddColumnOperation,
    ColumnOperation,
    DeleteColumnOperation,
    RenameColumnOperation,
)
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    ColumnWideConstraint,
)
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from skibidi_orm.exceptions.operations import UnsupportedOperationError
from typing import cast


class SQLite3ColumnOperationConverter(ColumnOperationSQLConverter):
    """Class responsible for converting column operation objects to raw SQLite3 SQL strings"""

    @staticmethod
    def convert_column_operation_to_SQL(operation: ColumnOperation) -> str:
        """Convert a given column operation to a SQLite3 SQL string"""
        if operation.operation_type == OperationType.CREATE:
            return SQLite3ColumnOperationConverter.convert_add_column_operation_to_SQL(
                cast(AddColumnOperation, operation)
            )
        elif operation.operation_type == OperationType.DELETE:
            return (
                SQLite3ColumnOperationConverter.convert_delete_column_operation_to_SQL(
                    cast(DeleteColumnOperation, operation)
                )
            )
        elif operation.operation_type == OperationType.RENAME:
            return (
                SQLite3ColumnOperationConverter.convert_rename_column_operation_to_SQL(
                    cast(RenameColumnOperation, operation)
                )
            )
        raise UnsupportedOperationError(
            "The given operation is not supported in SQLite3."
        )

    @staticmethod
    def convert_add_column_operation_to_SQL(operation: AddColumnOperation) -> str:
        """Convert a given add column operation to a SQLite3 SQL string"""
        column_definition = (
            SQLite3ColumnOperationConverter.convert_column_definition_to_SQL(
                operation.column, operation.column.column_constraints
            )
        )
        return_value = (
            f"ALTER TABLE {operation.table.name} ADD COLUMN {column_definition}"
        )
        if operation.related_foreign_key is not None:
            referenced_column = operation.related_foreign_key.column_mapping[
                operation.column.name
            ]
            fk_definition = f"REFERENCES {operation.related_foreign_key.referenced_table} ({referenced_column})"
            return_value += f" {fk_definition}"
        if operation.related_check_constraint is not None:
            check_definition = SQLite3ConstraintConverter.convert_constraint_to_SQL(
                operation.related_check_constraint
            )
            return_value += f" {check_definition}"

        return f"{return_value};"

    @staticmethod
    def convert_delete_column_operation_to_SQL(operation: DeleteColumnOperation) -> str:
        """Convert a given delete column operation to a SQLite3 SQL string"""
        return (
            f"ALTER TABLE {operation.table.name} DROP COLUMN {operation.column.name};"
        )

    @staticmethod
    def convert_rename_column_operation_to_SQL(operation: RenameColumnOperation) -> str:
        """Convert a given rename column operation to a SQLite3 SQL string"""
        return f"ALTER TABLE {operation.table.name} RENAME COLUMN {operation.column.name} TO {operation.new_name};"

    @staticmethod
    def convert_column_definition_to_SQL(
        column: SQLite3Typing.Column, constraints: list[ColumnWideConstraint]
    ) -> str:
        """Convert a given column definition to a SQLite3 SQL string"""
        return_value = f"{column.name} {column.data_type}"
        for constraint in constraints:
            return_value += (
                f" {SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint)}"
            )
        return return_value
