from typing import cast
from fastapi import FastAPI, Body
import uvicorn
from skibidi_orm.migration_engine.data_mutator.base_data_mutator import (
    BaseDataMutator,
    InsertRowColumn,
)
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector
from skibidi_orm.migration_engine.studio.utils.get_db_inspector import get_db_inspector
from skibidi_orm.migration_engine.studio.utils.get_db_seeder import get_db_seeder

app = FastAPI()
db_inspector: BaseDbInspector = cast(
    BaseDbInspector, {}
)  # to add db_inspector to modules namespace
db_seeder: BaseDataMutator = cast(
    BaseDataMutator, {}
)  # to add db_seeder to modules namespace


def run_server(schema_file: str):
    global db_inspector
    global db_seeder
    db_inspector = get_db_inspector(schema_file=schema_file)
    db_seeder = get_db_seeder(db_inspector)
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/db")
def get_db():
    tables = db_inspector.get_tables()
    return {"tables": tables}


@app.post("/db/{table_name}/row")
def insert_row(table_name: str, row: list[InsertRowColumn] = Body(embed=True)):
    if table_name not in db_inspector.get_tables_names():
        return {"message": "Table does not exist."}

    db_seeder.insert_row(table_name=table_name, row=row)
    return {"message": "Row inserted successfully."}
