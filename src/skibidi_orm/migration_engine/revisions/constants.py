from dotenv import load_dotenv
import os


"""Constants regarding revision managing, such as operations used to
create revision tables, etc."""

DEFAULT_REVISION_TABLE_NAME = "__revisions"


def get_revision_table_name() -> str:
    """Get the name of the table used to store revision data.
    If no name is set via an environment variable, the default name is used."""
    load_dotenv()
    return os.environ.get("__CHUMPY_REVISION_TABLE_NAME", DEFAULT_REVISION_TABLE_NAME)  # type: ignore
