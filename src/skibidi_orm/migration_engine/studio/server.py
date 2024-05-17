from typing import cast
from fastapi import FastAPI, Body
import uvicorn
from skibidi_orm.migration_engine.data_mutator.base_data_mutator import (
    BaseDataMutator,
    DeleteRowPk,
    InsertRowColumn,
)
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector
from skibidi_orm.migration_engine.studio.utils.get_db_inspector import get_db_inspector
from skibidi_orm.migration_engine.studio.utils.get_db_seeder import get_db_mutator

app = FastAPI()
db_inspector: BaseDbInspector = cast(
    BaseDbInspector, {}
)  # to add db_inspector to modules namespace
db_mutator: BaseDataMutator = cast(
    BaseDataMutator, {}
)  # to add db_seeder to modules namespace


def run_server(schema_file: str):
    global db_inspector
    global db_mutator
    db_inspector = get_db_inspector(schema_file=schema_file)
    db_mutator = get_db_mutator(db_inspector)
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/db")
def get_db():
    tables = db_inspector.get_tables()
    return {"tables": tables}


@app.post("/db/{table_name}/row")
def insert_row(table_name: str, row: list[InsertRowColumn] = Body(embed=True)):
    if table_name not in db_inspector.get_tables_names():
        return {"message": "Table does not exist."}

    db_mutator.insert_row(table_name=table_name, row=row)
    return {"message": "Row inserted successfully."}


@app.post("/db/{table_name}/row/delete")
def delete_row(table_name: str, pks: list[DeleteRowPk] = Body(embed=True)):
    if table_name not in db_inspector.get_tables_names():
        return {"message": "Table does not exist."}

    db_mutator.delete_row(table_name=table_name, pks=pks)
    return {"message": "Row deleted successfully."}
