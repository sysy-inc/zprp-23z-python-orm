import glob
from skibidi_orm.exceptions.cli_exceptions import MultipleSchemaFilesError

GLOB_ALL_SCHEMAS = "**/**/schema.py"


def find_schema_file():
    """
    Find the schema file in the project.
    If no schema file is found, raise FileNotFoundError.
    If multiple schema files are found, raise MultipleSchemaFilesError.
    """
    files = set(glob.glob(GLOB_ALL_SCHEMAS, recursive=True))
    if len(files) == 0:
        raise FileNotFoundError("No schema file found.")
    if len(files) > 1:
        raise MultipleSchemaFilesError("Multiple schema files found.")
    return files.pop()
