import pytest
import skibidi_orm.migration_engine.adapters.database_objects.constraints as c


def test_ColumnSpecificConstraint_sortable():
    try:
        sorted(
            [
                c.PrimaryKeyConstraint(
                    table_name="table_name",
                    column_name="column_name",
                ),
                c.NotNullConstraint(
                    table_name="table_name",
                    column_name="column_name",
                ),
            ]
        )
    except TypeError as e:
        pytest.fail(f"TypeError: {e}")
