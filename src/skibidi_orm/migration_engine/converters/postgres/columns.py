from skibidi_orm.migration_engine.adapters.postgres_typing import PostgresTyping
from skibidi_orm.migration_engine.converters.base.interfaces import (
    ColumnOperationSQLConverter,
)
from skibidi_orm.migration_engine.converters.postgres.constraints import (
    PostgresConstraintConverter,
)
from skibidi_orm.migration_engine.operations.column_operations import (
    AddColumnOperation,
    ColumnOperation,
    DeleteColumnOperation,
    RenameColumnOperation,
)
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    ColumnSpecificConstraint,
)
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from skibidi_orm.exceptions.operations import UnsupportedOperationError
from typing import cast


class PostgresColumnOperationConverter(ColumnOperationSQLConverter):
    """Class responsible for converting column operation objects to raw Postgres SQL strings"""

    @staticmethod
    def convert_column_operation_to_SQL(operation: ColumnOperation) -> str:
        """Convert a given column operation to a Postgres SQL string"""
        if operation.operation_type == OperationType.CREATE:
            return PostgresColumnOperationConverter.convert_add_column_operation_to_SQL(
                cast(AddColumnOperation, operation)
            )
        elif operation.operation_type == OperationType.DELETE:
            return (
                PostgresColumnOperationConverter.convert_delete_column_operation_to_SQL(
                    cast(DeleteColumnOperation, operation)
                )
            )
        elif operation.operation_type == OperationType.RENAME:
            return (
                PostgresColumnOperationConverter.convert_rename_column_operation_to_SQL(
                    cast(RenameColumnOperation, operation)
                )
            )
        raise UnsupportedOperationError(
            "The given operation is not supported in Postgres."
        )

    @staticmethod
    def convert_add_column_operation_to_SQL(operation: AddColumnOperation) -> str:
        """Convert a given add column operation to a Postgres SQL string"""
        column_definition = (
            PostgresColumnOperationConverter.convert_column_definition_to_SQL(
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

        return f"{return_value};"

    @staticmethod
    def convert_delete_column_operation_to_SQL(operation: DeleteColumnOperation) -> str:
        """Convert a given delete column operation to a Postgres SQL string"""
        return (
            f"ALTER TABLE {operation.table.name} DROP COLUMN {operation.column.name};"
        )

    @staticmethod
    def convert_rename_column_operation_to_SQL(operation: RenameColumnOperation) -> str:
        """Convert a given rename column operation to a Postgres SQL string"""
        return f"ALTER TABLE {operation.table.name} RENAME COLUMN {operation.column.name} TO {operation.new_name};"

    @staticmethod
    def convert_column_definition_to_SQL(
        column: PostgresTyping.Column, constraints: list[ColumnSpecificConstraint]
    ) -> str:
        """Convert a given column definition to a Postgres SQL string"""
        return_value = f"{column.name} {column.data_type}"
        for constraint in constraints:
            return_value += (
                f" {PostgresConstraintConverter.convert_constraint_to_SQL(constraint)}"
            )
        return return_value
