from skibidi_orm.migration_engine.adapters.sqlite3_typing import SQLite3Typing
from skibidi_orm.migration_engine.converters.base.interfaces import (
    TableOperationSQLConverter,
)
from skibidi_orm.migration_engine.converters.sqlite3.columns import (
    SQLite3ColumnOperationConverter,
)
from skibidi_orm.migration_engine.converters.sqlite3.constraints import (
    SQLite3ConstraintConverter,
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

        definition_string += "("
        for column in operation.table.columns:
            definition_string += f"{SQLite3ColumnOperationConverter.convert_column_definition_to_SQL(
                    column, column.column_constraints)}, "

        for key in operation.table.table_constraints:
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
            SQLite3Typing.Table(operation.new_name, operation.table.columns)
        )
        return (
            SQLite3TableOperationConverter.convert_table_operation_to_SQL(delete_op)
            + " "
            + SQLite3TableOperationConverter.convert_table_operation_to_SQL(create_op)
        )
