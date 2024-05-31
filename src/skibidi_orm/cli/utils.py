import glob
import os
from skibidi_orm.exceptions.cli_exceptions import MultipleSchemaFilesError
import importlib.util
import sys

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


def find_schema_file_with_a_given_path(path: str):
    """
    Find the schema file under the given path and return it in a .

    If no schema file is found, raise FileNotFoundError.
    """

    if os.path.exists(path):
        return path
    else:
        raise FileNotFoundError("No schema file found.")


def load_schema_from_path(path: str):
    """
    Load the schema file from the given path into the workspace.

    If schema file is not found, raise FileNotFoundError, if it cannot be imported, raise ImportError.
    It changes the current working directory to the specified path. Then it loads the schema file, and as a result,
    the absolute path of the database is relative to the schema file. After loading the schema file, it changes the
    current working directory back to the original one.
    """

    path = os.path.abspath(path)

    tmp_cwd = os.getcwd()
    os.chdir(os.path.dirname(path))

    path = find_schema_file_with_a_given_path(path)

    try:
        spec = importlib.util.spec_from_file_location("schema", path)
        module = importlib.util.module_from_spec(spec)  # type: ignore

        sys.modules["schema"] = module
        spec.loader.exec_module(module)  # type: ignore

    except ImportError:
        raise ImportError("Error while importing the schema file.")

    os.chdir(tmp_cwd)
