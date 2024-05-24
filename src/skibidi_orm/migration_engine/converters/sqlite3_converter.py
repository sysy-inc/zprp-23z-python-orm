from skibidi_orm.exceptions.constraints import UnsupportedConstraintError
from itertools import chain
from skibidi_orm.migration_engine.converters.sql_converter import (
    ColumnOperationSQLConverter,
    ConstraintSQLConverter,
    SQLConverter,
    TableOperationSQLConverter,
)
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.operations.column_operations import (
    AddColumnOperation,
    ColumnOperation,
    DeleteColumnOperation,
    RenameColumnOperation,
)
from skibidi_orm.migration_engine.operations.constraints import (
    CheckConstraint,
    ColumnSpecificConstraint,
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


class SQLite3TableOperationConverter(TableOperationSQLConverter):
    """Class responsible for converting table operation objects to raw SQLite3 SQL strings"""

    @staticmethod
    def convert_table_operation_to_SQL(operation: TableOperation) -> str:
        """Convert a given table operation to a SQLite3 SQL string"""
        if operation.operation_type == OperationType.CREATE:
            return (
                SQLite3TableOperationConverter._convert_create_table_operation_to_SQL(
                    cast(CreateTableOperation, operation)
                )
            )
        elif operation.operation_type == OperationType.DELETE:
            return SQLite3TableOperationConverter._convert_drop_table_operation_to_SQL(
                cast(DeleteTableOperation, operation)
            )
        elif operation.operation_type == OperationType.RENAME:
            return (
                SQLite3TableOperationConverter._convert_rename_table_operation_to_SQL(
                    cast(RenameTableOperation, operation)
                )
            )
        else:
            raise UnsupportedOperationError(
                "The given operation is not supported in SQLite3."
            )

    @staticmethod
    def _convert_create_table_operation_to_SQL(operation: CreateTableOperation) -> str:
        """Convert a given create table operation to a SQLite3 SQL string"""
        definition_string = f"CREATE TABLE {operation.table.name} "
        constraints_at_end, constraints_at_columns = SQLite3Converter.split_constraints(
            operation.table
        )

        definition_string += "("
        for column in operation.table.columns:
            constraints_at_column = [
                constraint
                for constraint in column.column_constraints
                if constraint in constraints_at_columns
            ]
            definition_string += f"{SQLite3ColumnOperationConverter.convert_column_definition_to_SQL(
                    column, constraints_at_column)}, "

        for constraint in constraints_at_end:
            definition_string += (
                f"{SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint)}, "
            )

        for key in operation.table.foreign_keys:
            definition_string += (
                f"{SQLite3ConstraintConverter.convert_constraint_to_SQL(key)}, "
            )

        return definition_string.strip(", ") + ");"

    @staticmethod
    def _convert_drop_table_operation_to_SQL(operation: DeleteTableOperation) -> str:
        """Convert a given drop table operation to a SQLite3 SQL string"""
        return f"DROP TABLE {operation.table.name};"

    @staticmethod
    def _convert_rename_table_operation_to_SQL(operation: RenameTableOperation) -> str:
        """Convert a given rename table operation to a SQLite3 SQL string. Since SQLite3 does not
        support renaming a table directly, a new table with the same columns has to be instantiated after
        deleting the original one."""
        delete_op = DeleteTableOperation(operation.table)
        create_op = CreateTableOperation(
            SQLite3Adapter.Table(operation.new_name, operation.table.columns)
        )
        return (
            SQLite3TableOperationConverter.convert_table_operation_to_SQL(delete_op)
            + " "
            + SQLite3TableOperationConverter.convert_table_operation_to_SQL(create_op)
        )


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
        column: SQLite3Adapter.Column, constraints: list[ColumnSpecificConstraint]
    ) -> str:
        """Convert a given column definition to a SQLite3 SQL string"""
        return_value = f"{column.name} {column.data_type}"
        for constraint in constraints:
            return_value += (
                f" {SQLite3ConstraintConverter.convert_constraint_to_SQL(constraint)}"
            )
        return return_value


class SQLite3ConstraintConverter(ConstraintSQLConverter):
    """Class responsible for converting constraint objects to raw SQLite3 SQL strings"""

    @staticmethod
    def convert_constraint_change_operation_to_SQL(_: Constraint) -> str:
        """Convert a given constraint change operation to a SQLite3 SQL string"""
        raise NotImplementedError(
            "Constraint change operations are not supported in SQLite3 yet."
        )

    @staticmethod
    def convert_constraint_to_SQL(constraint: Constraint) -> str:
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
        elif constraint.constraint_type == ConstraintType.NOT_NULL:
            return "NOT NULL"
        else:
            raise UnsupportedConstraintError(
                f"Constraints of type {constraint.constraint_type} are not supported by SQLite3"
            )


class SQLite3Converter(SQLConverter):
    """Class reponsible for converting operation and constraint
    objects to SQLite3 SQL strings"""

    @staticmethod
    def get_constraint_converter() -> type[ConstraintSQLConverter]:
        return SQLite3ConstraintConverter

    @staticmethod
    def get_table_operation_converter() -> type[TableOperationSQLConverter]:
        return SQLite3TableOperationConverter

    @staticmethod
    def get_column_operation_converter() -> type[ColumnOperationSQLConverter]:
        return SQLite3ColumnOperationConverter

    @staticmethod
    def split_constraints(
        table: SQLite3Adapter.Table,
    ) -> tuple[set[ColumnSpecificConstraint], set[ColumnSpecificConstraint]]:
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
                not in [ConstraintType.PRIMARY_KEY, ConstraintType.UNIQUE],
                all_constraints,
            )
        )

        # These constraints have to be added in the column definition
        constraints_at_columns = all_constraints - constraints_at_end

        return set(constraints_at_end), set(constraints_at_columns)
