import glob
from skibidi_orm.exceptions.cli_exceptions import MultipleSchemaFilesError

GLOB_ALL_SCHMEAS = "**/**/schema.py"


def find_schema_file():
    files = set(glob.glob(GLOB_ALL_SCHMEAS, recursive=True))
    if len(files) == 0:
        raise FileNotFoundError("No schema file found.")
    if len(files) > 1:
        raise MultipleSchemaFilesError("Multiple schema files found.")
    return files.pop()
