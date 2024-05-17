from fastapi import FastAPI
import uvicorn
from skibidi_orm.migration_engine.db_inspectors.base_inspector import BaseDbInspector
from skibidi_orm.migration_engine.studio.utils.get_db_inspector import get_db_inspector

app = FastAPI()
db_inspector: BaseDbInspector


def run_server(scheme_file: str):
    global db_inspector
    db_inspector = get_db_inspector(schema_file=scheme_file)
    uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/db")
def get_db():
    pass
