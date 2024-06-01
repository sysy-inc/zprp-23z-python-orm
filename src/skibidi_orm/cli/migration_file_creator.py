import os
from typing import Literal, TextIO, Any
from pathlib import Path
import black
from skibidi_orm.migration_engine.adapters.base_adapter import BaseColumn, BaseTable
from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)
from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.operations import table_operations as TO
from skibidi_orm.migration_engine.operations import column_operations as CO

type Typing = Literal["SQLite3Typing"]


def create_migration_file(migration_element: MigrationElement):
    """
    Inspect a migration element and create a Python file that can be executed to apply the migration.
    """
    migration_file_path = os.path.join(*[os.getcwd(), "migrations", "migration.py"])

    if not os.path.isdir(os.path.join(*[os.getcwd(), "migrations"])):
        os.mkdir(os.path.join(*[os.getcwd(), "migrations"]))

    config = BaseDbConfig.get_instance()

    migration_element.migrate(preview=True)

    operations = migration_element.operations

    if isinstance(config, SQLite3Config):
        executor = "SQLite3Executor"
        converter = "SQLite3Converter"
        typing = "SQLite3Typing"
    else:
        raise NotImplementedError

    operation_methods = extract_operation_methods(operations, typing)

    with open(migration_file_path, "w") as file:
        write_configuration(file)

        file.write("def migrate():\n")
        for method in operation_methods:

            if "TableOperation" in method:
                file.write(
                    f"\n\t{executor}.execute_sql(\n\t\t{converter}.convert_table_operation_to_SQL(\n\t\t\t{method}\n\t\t)\n\t)"
                )
            elif "ColumnOperation" in method:
                file.write(
                    f"\n\t{executor}.execute_sql({converter}.convert_column_operation_to_SQL({method}))"
                )
        if not operation_methods:
            file.write("\n\t# No operations to execute\n")
            file.write("\n\tpass")
        file.write("\n\n")

        file.write("if __name__ == '__main__':\n")
        file.write("\tmigrate()\n")

    black.format_file_in_place(
        Path(migration_file_path),
        fast=True,
        mode=black.FileMode(),
        write_back=black.WriteBack.YES,
    )


def extract_operation_methods(
    operations: list[CO.ColumnOperation | TO.TableOperation],
    typing: Typing,
) -> list[str]:
    """
    From a list of operations, extract proper strings of methods that can be executed in the migration file.
    """

    operation_methods: list[str] = []

    for operation in operations:
        if isinstance(operation, TO.TableOperation):
            operation_methods.append(parse_table_operation(operation, typing))
        else:
            operation_methods.append(parse_column_operation(operation, typing))

    return operation_methods


def write_configuration(file: TextIO):
    """
    Write the configuration for the migration file.
    """

    config = BaseDbConfig.get_instance()

    if isinstance(config, SQLite3Config):
        write_sqlite3_configuration(file)
    else:
        raise NotImplementedError

    file.write("# This is an auto-generated migration file.\n")
    file.write(
        "# Executing this file will result in executing the proposed migration.\n\n"
    )


def write_sqlite3_configuration(file: TextIO):
    """
    Write database specific configuration for SQLite3.
    """

    config = SQLite3Config.get_instance()

    file.write(
        """
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.sql_executor.sqlite3_executor import SQLite3Executor
from skibidi_orm.migration_engine.converters.sqlite3.all import SQLite3Converter
from skibidi_orm.migration_engine.adapters.database_objects import constraints as c
from skibidi_orm.migration_engine.adapters.sqlite3_typing import SQLite3Typing
from skibidi_orm.migration_engine.operations import table_operations as TO
from skibidi_orm.migration_engine.operations import column_operations as CO
"""
    )

    file.write("# Database: SQLite3\n")
    file.write(f"# Path: {config.db_path}\n\n")

    file.write("\n\n\n")
    file.write(f'SQLite3Config("{config.db_path}")')
    file.write("\n\n\n")


def parse_column_operation(operation: CO.ColumnOperation, typing: Typing) -> str:
    """
    Parse a ColumnOperation object to get a creatable string
    """
    operation_str = ""

    column = operation.column

    column_str = return_column_string(column, typing)

    table_str = return_table_string(operation.table, typing)

    if isinstance(operation, CO.RenameColumnOperation):
        operation_str = f"CO.{operation.__class__.__name__}(table={table_str}, column={column_str}, new_name='{operation.new_name}')"
    else:
        operation_str = (
            f"CO.{operation.__class__.__name__}(table={table_str}, column={column_str})"
        )

    return operation_str


def parse_table_operation(operation: TO.TableOperation, typing: Typing) -> str:
    """
    Parse a TableOperation object to get a creatable string
    """
    operation_str = ""
    table_str = ""

    table_str = return_table_string(operation.table, typing)

    if isinstance(operation, TO.RenameTableOperation):
        operation_str = f"TO.{operation.__class__.__name__}(table={table_str}, new_name='{operation.new_name}')"
    else:
        operation_str = f"TO.{operation.__class__.__name__}(table={table_str})"

    return operation_str


def return_column_string(column: BaseColumn[Any], typing: Typing) -> str:
    """
    Return a string that can construct a column object.
    """

    constraints_str = return_constraint_list_string(column, typing)

    return f"{typing}.Column(name='{column.name}', data_type='{column.data_type}', column_constraints={constraints_str},),"


def return_constraint_list_string(column: BaseColumn[Any], typing: Typing) -> str:
    """
    Return a string representation of a list of constraints.
    """
    constraints_str = "["

    for constraint in column.column_constraints:
        constraints_str += f"c.{constraint}, "
    constraints_str = constraints_str[:-2] + "]"

    return constraints_str


def return_table_string(table: BaseTable[BaseColumn[Any]], typing: Typing) -> str:
    """
    Return a string that can create a table object.
    """
    columns_str = "["
    for column in table.columns:
        columns_str += return_column_string(column, typing)
    columns_str += "]"

    return f"{typing}.Table(name='{table.name}', columns={columns_str})"
