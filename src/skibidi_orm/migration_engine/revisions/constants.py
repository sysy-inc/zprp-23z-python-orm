from dotenv import load_dotenv


"""Constants regarding revision managing, such as operations used to
create revision tables, etc."""

DEFAULT_REVISION_TABLE_NAME = "__revisions"

REVISION_TABLE_COLUMN_NAMES = (
    "id",
    "timestamp",
    "description",
    "schema_repr",
    "config_data",
    "schema_data",
    "__internal",
)


def get_revision_table_name() -> str:
    """Get the name of the table used to store revision data.
    If no name is set via an environment variable, the default name is used."""
    load_dotenv()

    try:
        return __CHUMPY_REVISION_TABLE_NAME  # type: ignore
    except NameError:
        return DEFAULT_REVISION_TABLE_NAME
