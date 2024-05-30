import skibidi_orm.migration_engine.adapters.database_objects.constraints as c


def test_ColumnSpecificConstraint_sortable():
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
            c.CheckConstraint(
                table_name="table_name",
                column_name="column_name",
                condition="condition",
            ),
        ]
    )
    assert True
