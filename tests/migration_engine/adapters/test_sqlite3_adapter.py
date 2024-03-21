import pytest
from src.migration_engine.adapters.sqlite3_adapter import SQLite3Adapter


class TestSQLite3Adapter:

    def setup_method(self):
        self.adapter = SQLite3Adapter()

    def test_create_column(self):
        column = SQLite3Adapter.Column("id", "INTEGER", ["PRIMARY KEY"])
        assert column.name == "id"
        assert column.data_type == "INTEGER"
        assert column.constraints == ["PRIMARY KEY"]

    def test_create_column_without_constraints(self):
        column = SQLite3Adapter.Column("name", "TEXT")
        assert column.name == "name"
        assert column.data_type == "TEXT"
        assert len(column.constraints) == 0

    # def test_create_column_wrong_data_type(self):
    #     SQLite3Adapter.Column("id", "INT")


if __name__ == "__main__":
    pytest.main()
