from zprp_23z_python_orm.migration_engine.base_table import BaseTable
from zprp_23z_python_orm.migration_engine.table_example import (
    Table,
)  # required to initialize the schema file


if __name__ == "__main__":
    BaseTable.migrate()
