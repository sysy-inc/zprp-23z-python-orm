from base_table import BaseTable
from table_example import Table  # required to initialize the schema file


if __name__ == "__main__":
    BaseTable.migrate()
