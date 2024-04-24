from skibidi_orm.exceptions.constraints_exceptions import UnsupportedConstraintError
from skibidi_orm.migration_engine.adapters.base_adapter import BaseColumn
from skibidi_orm.migration_engine.converters.sql_converter import SQLConverter
from skibidi_orm.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter
from skibidi_orm.migration_engine.operations.column_operations import (
    AddColumnOperation,
    ChangeDataTypeOperation,
    ColumnOperation,
    DeleteColumnOperation,
    RenameColumnOperation,
)
from skibidi_orm.migration_engine.adapters.database_objects.constraints import (
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
from skibidi_orm.exceptions.operations_exceptions import UnsupportedOperationError
from typing import cast
from itertools import chain


class SQLite3Converter(SQLConverter):
    """Class reponsible for converting operation and constraint
    objects to SQLite3 SQL strings"""

    @staticmethod
    def convert_table_operation_to_SQL(operation: TableOperation) -> str:
        """Convert a given table operation to a SQLite3 SQL string"""
        if operation.operation_type == OperationType.CREATE:
            return SQLite3Converter._convert_create_table_operation_to_SQL(
                cast(CreateTableOperation, operation)
            )
        elif operation.operation_type == OperationType.DELETE:
            return SQLite3Converter._convert_drop_table_operation_to_SQL(
                cast(DeleteTableOperation, operation)
            )
        elif operation.operation_type == OperationType.RENAME:
            return SQLite3Converter._convert_rename_table_operation_to_SQL(
                cast(RenameTableOperation, operation)
            )
        else:
            raise UnsupportedOperationError(
                "The given operation is not supported in SQLite3."
            )

    @staticmethod
    def convert_column_operation_to_SQL(operation: ColumnOperation) -> str:
        """Convert a given column operation to a SQLite3 SQL string"""
        if operation.operation_type == OperationType.CREATE:
            return SQLite3Converter.convert_add_column_operation_to_SQL(
                cast(AddColumnOperation, operation)
            )
        elif operation.operation_type == OperationType.DELETE:
            return SQLite3Converter.convert_delete_column_operation_to_SQL(
                cast(DeleteColumnOperation, operation)
            )
        elif operation.operation_type == OperationType.RENAME:
            return SQLite3Converter.convert_rename_column_operation_to_SQL(
                cast(RenameColumnOperation, operation)
            )
        elif operation.operation_type == OperationType.DTYPE_CHANGE:
            return SQLite3Converter.convert_dtype_change_operation_to_SQL(
                cast(ChangeDataTypeOperation, operation)
            )
        # TODO: constraint change
        elif operation.operation_type == OperationType.CONSTRAINT_CHANGE:
            return SQLite3Converter.convert_constraint_change_operation_to_SQL(
                cast(Constraint, operation)
            )
        raise UnsupportedOperationError(
            "The given operation is not supported in SQLite3."
        )

    @staticmethod
    def convert_add_column_operation_to_SQL(operation: AddColumnOperation) -> str:
        """Convert a given add column operation to a SQLite3 SQL string"""
        return f"ALTER TABLE {operation.table.name} ADD COLUMN {SQLite3Converter.convert_column_definition_to_SQL(operation.column, operation.column.constraints)};"

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
    def convert_dtype_change_operation_to_SQL(
        operation: ChangeDataTypeOperation,
    ) -> str:
        """Convert a given data type change operation to a SQLite3 SQL string"""
        delete_op = DeleteColumnOperation(operation.table, operation.column)
        add_op = AddColumnOperation(
            operation.table,
            BaseColumn(
                name=operation.column.name,
                data_type=operation.new_dtype,
                constraints=operation.column.constraints,
            ),
        )
        return (
            SQLite3Converter.convert_column_operation_to_SQL(delete_op)
            + " "
            + SQLite3Converter.convert_column_operation_to_SQL(add_op)
        )

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
        else:
            raise UnsupportedConstraintError(
                f"Constraints of type {constraint.constraint_type} are not supported by SQLite3"
            )

    @staticmethod
    def _convert_create_table_operation_to_SQL(operation: CreateTableOperation) -> str:
        """Convert a given create table operation to a SQLite3 SQL string"""
        definition_string = f"CREATE TABLE {operation.table.name}"
        constraints_at_end, constraints_at_columns = SQLite3Converter.split_constraints(
            operation.table
        )
        # TODO: refactor
        column_listing = ", ".join(
            SQLite3Converter.convert_column_definition_to_SQL(
                column,
                [
                    constraint
                    for constraint in column.constraints
                    if constraint in constraints_at_columns
                ],
            )
            for column in operation.table.columns
        )

        constraints_at_end = ", ".join(
            SQLite3Converter.convert_constraint_to_SQL(constraint)
            for constraint in constraints_at_end
        )
        return " ".join(
            element
            for element in (
                definition_string,
                f"({', '.join(string for string in (column_listing, constraints_at_end) if string)});",
            )
        )

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
            SQLite3Converter.convert_table_operation_to_SQL(delete_op)
            + " "
            + SQLite3Converter.convert_table_operation_to_SQL(create_op)
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

    @staticmethod
    def convert_column_definition_to_SQL(
        column: SQLite3Adapter.Column, constraints: list[Constraint]
    ) -> str:
        """Convert a given column definition to a SQLite3 SQL string"""

        return " ".join(
            element
            for element in (
                f"{column.name} {column.data_type}",
                " ".join(
                    (
                        # TODO: refactor to not call convert constraint twice
                        SQLite3Converter.convert_constraint_to_SQL(constraint)
                        if constraint.constraint_type != ConstraintType.FOREIGN_KEY
                        else SQLite3Converter.convert_constraint_to_SQL(
                            constraint
                        ).split(maxsplit=3)[-1]
                    )
                    for constraint in constraints
                ),
            )
            if element
        )
