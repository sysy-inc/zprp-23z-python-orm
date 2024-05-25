from typing import cast
from fastapi import FastAPI, Body
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from skibidi_orm.migration_engine.data_mutator.base_data_mutator import (
    BaseDataMutator,
    DeleteRowPk,
    InsertRowColumn,
)
from fastapi.middleware.cors import CORSMiddleware
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/assets",
    StaticFiles(
        directory="src/skibidi_orm/migration_engine/studio/skibidi-orm-studio-frontend/dist/assets"
    ),
    name="static",
)


def run_server(schema_file: str):
    global db_inspector
    global db_mutator
    db_inspector = get_db_inspector(schema_file=schema_file)
    db_mutator = get_db_mutator(db_inspector)
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/")
def read_index():
    return FileResponse(
        "src/skibidi_orm/migration_engine/studio/skibidi-orm-studio-frontend/dist/index.html"
    )


@app.get("/db")
def get_db():
    """Get the tables in the database."""
    tables = db_inspector.get_tables()
    return {"tables": tables}


@app.post("/db/{table_name}/row")
def insert_row(table_name: str, row: list[InsertRowColumn] = Body(embed=True)):
    """Insert a row in the table."""
    if table_name not in db_inspector.get_tables_names():
        return {"message": "Table does not exist."}

    db_mutator.insert_row(table_name=table_name, row=row)
    return {"message": "Row inserted successfully."}


@app.post("/db/{table_name}/row/delete")
def delete_row(table_name: str, pks: list[DeleteRowPk] = Body(embed=True)):
    """Delete a row in the table. Row identified by primary key subset."""
    if table_name not in db_inspector.get_tables_names():
        return {"message": "Table does not exist."}

    db_mutator.delete_row(table_name=table_name, pks=pks)
    return {"message": "Row deleted successfully."}


@app.post("/db/query")
def query_table(query: str = Body(embed=True)):
    """Execute a raw sql query in the database."""
    results = db_mutator.raw_query(query)
    return results


@app.get("/db/{table_name}/rows")
def get_rows(table_name: str, offset: int = 0, limit: int = 100):
    """Get paginated rows from the table."""
    if table_name not in db_inspector.get_tables_names():
        return {"message": "Table does not exist."}

    rows = db_mutator.get_rows(table_name, offset=offset, limit=limit)
    return rows
