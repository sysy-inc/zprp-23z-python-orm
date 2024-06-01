from skibidi_orm.migration_engine.adapters.postgres_typing import PostgresTyping
from skibidi_orm.migration_engine.converters.base.interfaces import (
    TableOperationSQLConverter,
)
from skibidi_orm.migration_engine.converters.postgres.columns import PostgresColumnOperationConverter
from skibidi_orm.migration_engine.converters.postgres.constraints import PostgresConstraintConverter
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
    ColumnWideConstraint,
    ConstraintType,
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


class PostgresTableOperationConverter(TableOperationSQLConverter):
    """Class responsible for converting table operation objects to raw Postgres SQL strings"""

    @staticmethod
    def convert_table_operation_to_SQL(operation: TableOperation) -> str:
        """Convert a given table operation to a Postgres SQL string"""
        if operation.operation_type == OperationType.CREATE:
            return (
                PostgresTableOperationConverter._convert_create_table_operation_to_SQL(
                    cast(CreateTableOperation, operation)
                )
            )
        elif operation.operation_type == OperationType.DELETE:
            return PostgresTableOperationConverter._convert_drop_table_operation_to_SQL(
                cast(DeleteTableOperation, operation)
            )
        elif operation.operation_type == OperationType.RENAME:
            return (
                PostgresTableOperationConverter._convert_rename_table_operation_to_SQL(
                    cast(RenameTableOperation, operation)
                )
            )
        else:
            raise UnsupportedOperationError(
                "The given operation is not supported in Postgres."
            )

    @staticmethod
    def _convert_create_table_operation_to_SQL(operation: CreateTableOperation) -> str:
        """Convert a given create table operation to a Postgres SQL string"""
        definition_string = f"CREATE TABLE {operation.table.name} "
        constraints_at_end, constraints_at_columns = (
            PostgresTableOperationConverter.split_constraints(operation.table)
        )

        definition_string += "("
        for column in operation.table.columns:
            constraints_at_column = [
                constraint
                for constraint in column.column_constraints
                if constraint in constraints_at_columns
            ]
            definition_string += f"{PostgresColumnOperationConverter.convert_column_definition_to_SQL(
                    column, constraints_at_column)}, "

        for constraint in constraints_at_end:
            definition_string += (
                f"{PostgresConstraintConverter.convert_constraint_to_SQL(constraint)}, "
            )

        for key in operation.table.table_constraints:
            definition_string += (
                f"{PostgresConstraintConverter.convert_constraint_to_SQL(key)}, "
            )

        return definition_string.strip(", ") + ");"

    @staticmethod
    def _convert_drop_table_operation_to_SQL(operation: DeleteTableOperation) -> str:
        """Convert a given drop table operation to a Postgres SQL string"""
        return f"DROP TABLE {operation.table.name};"

    @staticmethod
    def _convert_rename_table_operation_to_SQL(operation: RenameTableOperation) -> str:
        """Convert a given rename table operation to a Postgres SQL string. Since Postgres does not
        support renaming a table directly, a new table with the same columns has to be instantiated after
        deleting the original one."""
        delete_op = DeleteTableOperation(operation.table)
        create_op = CreateTableOperation(
            PostgresTyping.Table(operation.new_name, operation.table.columns)
        )
        return (
            PostgresTableOperationConverter.convert_table_operation_to_SQL(delete_op)
            + " "
            + PostgresTableOperationConverter.convert_table_operation_to_SQL(create_op)
        )

    @staticmethod
    def split_constraints(
        table: PostgresTyping.Table,
    ) -> tuple[set[ColumnWideConstraint], set[ColumnWideConstraint]]:
        """Split the constraints of a table into those that have to be added at the end of the
        table definition and those that have to be added in the definitions of their resective columns
        """
        all_constraints = set(
            chain.from_iterable(column.column_constraints for column in table.columns)
        )

        """These constraints have to be added at the end of the table definition, not by the
        columns they correspond to"""
        constraints_at_end = set(
            filter(
                lambda c: c.constraint_type
                not in [ConstraintType.PRIMARY_KEY, ConstraintType.UNIQUE, ConstraintType.NOT_NULL],
                all_constraints,
            )
        )

        # These constraints have to be added in the column definition
        constraints_at_columns = all_constraints - constraints_at_end

        return set(constraints_at_end), set(constraints_at_columns)
