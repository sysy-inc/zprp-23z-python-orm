from skibidi_orm.migration_engine.operations.table_operations import *
from skibidi_orm.migration_engine.operations.column_operations import *
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from skibidi_orm.migration_engine.operations.constraints import *
from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable, BaseColumn
from typing import Literal
from pytest import raises

DataType = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
mock_table_1 = BaseTable[BaseColumn[DataType]]("table")
mock_table_2 = BaseTable[BaseColumn[DataType]]("table_2")
mock_column_1 = BaseColumn[DataType]("column", "INTEGER")
mock_column_2 = BaseColumn[DataType]("column_2", "TEXT")


def test_create_table_operation_init_reverse():
    operation = CreateTableOperation(table=mock_table_1)
    assert operation.operation_type == OperationType.CREATE
    assert operation.table == mock_table_1
    assert operation.is_reversible is True

    reverse_operation = operation.reverse()
    assert reverse_operation == DeleteTableOperation(table=operation.table)


def test_delete_table_operation_init_reverse():
    operation = DeleteTableOperation(table=mock_table_1)
    assert operation.operation_type == OperationType.DELETE
    assert operation.table == mock_table_1
    assert operation.is_reversible is False

    with raises(IrreversibleOperationError):
        operation.reverse()


def test_rename_table_operation_init_reverse():
    operation = RenameTableOperation(table=mock_table_1, new_name=mock_table_2.name)
    assert operation.operation_type == OperationType.RENAME
    assert operation.table == mock_table_1
    assert operation.new_name == mock_table_2.name
    assert operation.is_reversible is True
    assert operation.reverse() == RenameTableOperation(
        table=mock_table_1, new_name=mock_table_1.name
    )


def test_add_column_operation_init_reverse():
    operation = AddColumnOperation(table=mock_table_1, column=mock_column_1)
    assert operation.operation_type == OperationType.CREATE
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.is_reversible is True

    reverse_operation = operation.reverse()
    assert reverse_operation == DeleteColumnOperation(
        table=operation.table,
        column=operation.column,
    )


def test_delete_column_operation_init_reverse():
    operation = DeleteColumnOperation(table=mock_table_1, column=mock_column_1)
    assert operation.operation_type == OperationType.DELETE
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.is_reversible is False
    with raises(IrreversibleOperationError):
        operation.reverse()


def test_rename_column_operation_init_reverse():
    operation = RenameColumnOperation(
        table=mock_table_1,
        column=mock_column_1,
        new_name=mock_column_2.name,
    )
    assert operation.operation_type == OperationType.RENAME
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.new_name == mock_column_2.name
    assert operation.is_reversible is True
    assert operation.reverse() == RenameColumnOperation(
        table=mock_table_1,
        column=mock_column_1,
        new_name=mock_column_1.name,
    )


def test_add_constraint_operation_init_reverse():
    operation = AddConstraintOperation(
        table=mock_table_1,
        column=mock_column_1,
        constraint=PrimaryKeyConstraint(),
    )
    assert operation.operation_type == OperationType.CONSTRAINT_CHANGE
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.constraint == PrimaryKeyConstraint()
    assert operation.is_reversible is True

    reverse_operation = operation.reverse()
    assert reverse_operation == DeleteConstraintOperation(
        table=operation.table,
        column=operation.column,
        constraint=operation.constraint,
    )


def test_delete_constraint_operation_init_reverse():
    operation = DeleteConstraintOperation(
        table=mock_table_1,
        column=mock_column_1,
        constraint=PrimaryKeyConstraint(),
    )
    assert operation.operation_type == OperationType.CONSTRAINT_CHANGE
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.constraint == PrimaryKeyConstraint()
    assert operation.is_reversible is True
    reverse_operation = operation.reverse()
    assert reverse_operation == AddConstraintOperation(
        table=operation.table,
        column=operation.column,
        constraint=operation.constraint,
    )


def test_change_data_type_operation_init_reverse():
    operation = ChangeDataTypeOperation(
        table=mock_table_1,
        column=mock_column_1,
        new_dtype=mock_column_2.data_type,
    )
    assert operation.operation_type == OperationType.DTYPE_CHANGE
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.new_dtype == mock_column_2.data_type
    assert operation.is_reversible is True
    assert operation.reverse() == ChangeDataTypeOperation(
        table=mock_table_1,
        column=mock_column_1,
        new_dtype=mock_column_1.data_type,
    )
