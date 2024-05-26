from skibidi_orm.exceptions.operations import IrreversibleOperationError
import skibidi_orm.migration_engine.operations.table_operations as t_ops
import skibidi_orm.migration_engine.operations.column_operations as c_ops
from skibidi_orm.migration_engine.operations.operation_type import OperationType
import skibidi_orm.migration_engine.adapters.database_objects.constraints as c
from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable, BaseColumn
from typing import Literal
from pytest import raises

DataType = Literal["TEXT", "INTEGER", "REAL", "BLOB", "NULL"]
mock_table_1 = BaseTable[BaseColumn[DataType]]("table")
mock_table_2 = BaseTable[BaseColumn[DataType]]("table_2")
mock_column_1 = BaseColumn[DataType]("column", "INTEGER")
mock_column_2 = BaseColumn[DataType]("column_2", "TEXT")


def test_create_table_operation_init_reverse():
    operation = t_ops.CreateTableOperation(table=mock_table_1)
    assert operation.operation_type == OperationType.CREATE
    assert operation.table == mock_table_1
    assert operation.is_reversible is True

    reverse_operation = operation.reverse()
    assert reverse_operation == t_ops.DeleteTableOperation(table=operation.table)


def test_delete_table_operation_init_reverse():
    operation = t_ops.DeleteTableOperation(table=mock_table_1)
    assert operation.operation_type == OperationType.DELETE
    assert operation.table == mock_table_1
    assert operation.is_reversible is False

    with raises(IrreversibleOperationError):
        operation.reverse()


def test_rename_table_operation_init_reverse():
    operation = t_ops.RenameTableOperation(
        table=mock_table_1, new_name=mock_table_2.name
    )
    assert operation.operation_type == OperationType.RENAME
    assert operation.table == mock_table_1
    assert operation.new_name == mock_table_2.name
    assert operation.is_reversible is True
    assert operation.reverse() == t_ops.RenameTableOperation(
        table=mock_table_1, new_name=mock_table_1.name
    )


def test_add_column_operation_init_reverse():
    operation = c_ops.AddColumnOperation(table=mock_table_1, column=mock_column_1)
    assert operation.operation_type == OperationType.CREATE
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.is_reversible is True

    reverse_operation = operation.reverse()
    assert reverse_operation == c_ops.DeleteColumnOperation(
        table=operation.table,
        column=operation.column,
    )


def test_add_column_composite_foreign_key():
    """Shouldn't be able to initialise an c_ops.AddColumnOperation with a composite foreign key."""
    with raises(ValueError):
        c_ops.AddColumnOperation(
            table=mock_table_1,
            column=mock_column_1,
            related_foreign_key=c.ForeignKeyConstraint(
                mock_table_1.name,
                mock_table_2.name,
                {
                    "composite": "key",
                    mock_column_1.name: mock_column_2.name,
                },
            ),
        )


def test_add_column_foreign_key_references_different_column():
    """Shouldn't be able to initialise an c_ops.AddColumnOperation with a foreign key that references a different column."""
    with raises(ValueError):
        c_ops.AddColumnOperation(
            table=mock_table_1,
            column=mock_column_1,
            related_foreign_key=c.ForeignKeyConstraint(
                mock_table_1.name,
                mock_table_2.name,
                {
                    mock_column_2.name: "this should throw an exception",
                },
            ),
        )


def test_add_column_foreign_key_references_different_table():
    """Shouldn't be able to initialise an c_ops.AddColumnOperation with a foreign key that references the wrong table."""
    with raises(ValueError):
        c_ops.AddColumnOperation(
            table=mock_table_1,
            column=mock_column_1,
            related_foreign_key=c.ForeignKeyConstraint(
                mock_table_2.name,
                "this should throw an exception",
                {
                    mock_column_1.name: mock_column_2.name,
                },
            ),
        )


def test_delete_column_operation_init_reverse():
    operation = c_ops.DeleteColumnOperation(table=mock_table_1, column=mock_column_1)
    assert operation.operation_type == OperationType.DELETE
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.is_reversible is False
    with raises(IrreversibleOperationError):
        operation.reverse()


def test_rename_column_operation_init_reverse():
    operation = c_ops.RenameColumnOperation(
        table=mock_table_1,
        column=mock_column_1,
        new_name=mock_column_2.name,
    )
    assert operation.operation_type == OperationType.RENAME
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.new_name == mock_column_2.name
    assert operation.is_reversible is True
    assert operation.reverse() == c_ops.RenameColumnOperation(
        table=mock_table_1,
        column=mock_column_1,
        new_name=mock_column_1.name,
    )


def test_add_constraint_operation_init_reverse():
    operation = c_ops.AddConstraintOperation(
        table=mock_table_1,
        column=mock_column_1,
        constraint=c.PrimaryKeyConstraint(mock_table_1.name, mock_column_1.name),
    )
    assert operation.operation_type == OperationType.CONSTRAINT_CHANGE
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.constraint == c.PrimaryKeyConstraint(
        mock_table_1.name, mock_column_1.name
    )
    assert operation.is_reversible is True

    reverse_operation = operation.reverse()
    assert reverse_operation == c_ops.DeleteConstraintOperation(
        table=operation.table,
        column=operation.column,
        constraint=operation.constraint,
    )


def test_delete_constraint_operation_init_reverse():
    operation = c_ops.DeleteConstraintOperation(
        table=mock_table_1,
        column=mock_column_1,
        constraint=c.PrimaryKeyConstraint(mock_table_1.name, mock_column_1.name),
    )
    assert operation.operation_type == OperationType.CONSTRAINT_CHANGE
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.constraint == c.PrimaryKeyConstraint(
        mock_table_1.name, mock_column_1.name
    )
    assert operation.is_reversible is True
    reverse_operation = operation.reverse()
    assert reverse_operation == c_ops.AddConstraintOperation(
        table=operation.table,
        column=operation.column,
        constraint=operation.constraint,
    )


def test_change_data_type_operation_init_reverse():
    operation = c_ops.ChangeDataTypeOperation(
        table=mock_table_1,
        column=mock_column_1,
        new_dtype=mock_column_2.data_type,
    )
    assert operation.operation_type == OperationType.DTYPE_CHANGE
    assert operation.table == mock_table_1
    assert operation.column == mock_column_1
    assert operation.new_dtype == mock_column_2.data_type
    assert operation.is_reversible is True
    assert operation.reverse() == c_ops.ChangeDataTypeOperation(
        table=mock_table_1,
        column=mock_column_1,
        new_dtype=mock_column_1.data_type,
    )
