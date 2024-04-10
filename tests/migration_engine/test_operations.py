from skibidi_orm.migration_engine.operations.table_operations import *
from skibidi_orm.migration_engine.operations.column_operations import *
from skibidi_orm.migration_engine.operations.operation_type import OperationType
from skibidi_orm.migration_engine.operations.constraints import *
from pytest import raises

mock_table_name_1 = "table_name"
mock_table_name_2 = "table_name_2"
mock_column_name_1 = "column_name"
mock_column_name_2 = "column_name_2"
data_type_1 = "INTEGER"
data_type_2 = "TEXT"


def test_create_table_operation_init_reverse():
    operation = CreateTableOperation(table_name=mock_table_name_1)
    assert operation.operation_type == OperationType.CREATE
    assert operation.table_name == mock_table_name_1
    assert operation.is_reversible is True

    reverse_operation = operation.reverse()
    assert reverse_operation == DeleteTableOperation(table_name=operation.table_name)


def test_delete_table_operation_init_reverse():
    operation = DeleteTableOperation(table_name=mock_table_name_1)
    assert operation.operation_type == OperationType.DELETE
    assert operation.table_name == mock_table_name_1
    assert operation.is_reversible is False

    with raises(IrreversibleOperationError):
        operation.reverse()


def test_rename_table_operation_init_reverse():
    operation = RenameTableOperation(
        table_name=mock_table_name_1, new_name=mock_table_name_2
    )
    assert operation.operation_type == OperationType.RENAME
    assert operation.table_name == mock_table_name_1
    assert operation.new_name == mock_table_name_2
    assert operation.is_reversible is True
    assert operation.reverse() == RenameTableOperation(
        table_name=mock_table_name_2, new_name=mock_table_name_1
    )


def test_add_column_operation_init_reverse():
    operation = AddColumnOperation(
        table_name=mock_table_name_1, column_name=mock_column_name_1
    )
    assert operation.operation_type == OperationType.CREATE
    assert operation.table_name == mock_table_name_1
    assert operation.column_name == mock_column_name_1
    assert operation.is_reversible is True

    reverse_operation = operation.reverse()
    assert reverse_operation == DeleteColumnOperation(
        table_name=operation.table_name,
        column_name=operation.column_name,
    )


def test_delete_column_operation_init_reverse():
    operation = DeleteColumnOperation(
        table_name=mock_table_name_1, column_name=mock_column_name_1
    )
    assert operation.operation_type == OperationType.DELETE
    assert operation.table_name == mock_table_name_1
    assert operation.column_name == mock_column_name_1
    assert operation.is_reversible is False
    with raises(IrreversibleOperationError):
        operation.reverse()


def test_rename_column_operation_init_reverse():
    operation = RenameColumnOperation(
        table_name=mock_table_name_1,
        column_name=mock_column_name_1,
        new_name=mock_column_name_2,
    )
    assert operation.operation_type == OperationType.RENAME
    assert operation.table_name == mock_table_name_1
    assert operation.column_name == mock_column_name_1
    assert operation.new_name == mock_column_name_2
    assert operation.is_reversible is True
    assert operation.reverse() == RenameColumnOperation(
        table_name=mock_table_name_1,
        column_name=mock_column_name_2,
        new_name=mock_column_name_1,
    )


def test_add_constraint_operation_init_reverse():
    operation = AddConstraintOperation(
        table_name=mock_table_name_1,
        column_name=mock_column_name_1,
        constraint=PrimaryKeyConstraint(),
    )
    assert operation.operation_type == OperationType.CONSTRAINT_CHANGE
    assert operation.table_name == mock_table_name_1
    assert operation.column_name == mock_column_name_1
    assert operation.constraint == PrimaryKeyConstraint()
    assert operation.is_reversible is True

    reverse_operation = operation.reverse()
    assert reverse_operation == DeleteConstraintOperation(
        table_name=operation.table_name,
        column_name=operation.column_name,
        constraint=operation.constraint,
    )


def test_delete_constraint_operation_init_reverse():
    operation = DeleteConstraintOperation(
        table_name=mock_table_name_1,
        column_name=mock_column_name_1,
        constraint=PrimaryKeyConstraint(),
    )
    assert operation.operation_type == OperationType.CONSTRAINT_CHANGE
    assert operation.table_name == mock_table_name_1
    assert operation.column_name == mock_column_name_1
    assert operation.constraint == PrimaryKeyConstraint()
    assert operation.is_reversible is True
    reverse_operation = operation.reverse()
    assert reverse_operation == AddConstraintOperation(
        table_name=operation.table_name,
        column_name=operation.column_name,
        constraint=operation.constraint,
    )


def test_change_data_type_operation_init_reverse():
    operation = ChangeDataTypeOperation(
        table_name=mock_table_name_1,
        column_name=mock_column_name_1,
        old_dtype=data_type_1,
        new_dtype=data_type_2,
    )
    assert operation.operation_type == OperationType.DTYPE_CHANGE
    assert operation.table_name == mock_table_name_1
    assert operation.column_name == mock_column_name_1
    assert operation.old_dtype == data_type_1
    assert operation.new_dtype == data_type_2
    assert operation.is_reversible is True
    assert operation.reverse() == ChangeDataTypeOperation(
        table_name=mock_table_name_1,
        column_name=mock_column_name_1,
        old_dtype=data_type_2,
        new_dtype=data_type_1,
    )
