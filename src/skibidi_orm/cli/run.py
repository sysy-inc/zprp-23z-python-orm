# This file can by run by executing `skibidi-orm` in the terminal, after the package is installed.
# `skibidi-orm migrate [--message <STRING>]`
# `skibidi-orm list-migrations`
# `skibidi-orm go <MIGRATION_ID>`


import typer
from typing import Union
import os

# import shutil
import sys
from skibidi_orm.cli.utils import find_schema_file
from skibidi_orm.exceptions.cli_exceptions import MultipleSchemaFilesError
from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
from skibidi_orm.migration_engine.revisions.manager import RevisionManager
from skibidi_orm.migration_engine.studio.server import run_server
from skibidi_orm.cli.revision_inspection import revision_app  # type: ignore
from colorama import Fore

sys.path.insert(0, os.getcwd())


app = typer.Typer(
    help="CLI tool for managing schema creations and migrations in Skibidi ORM."
)


@app.command()
def migrate(
    message: str = typer.Option(
        None, "--message", "-m", help="Description of migration"
    )
):
    """
    Used to run migration for current schema file. Can accept an optional message as a description of the migration.
    """
    m = MigrationElement()
    m.migrate(preview=False)
    pass


@app.command(name="preview-migration")
def preview_migration():
    """
    Preview the migration that will be executed.
    """
    m = MigrationElement()
    m.migrate(preview=True)

    if not m.operations:
        print("No changes to be made.")
    else:
        for i, operation in enumerate(m.operations):
            print(f"{i+1}) {operation}")
    pass


@app.command(name="log")
def migrate_list():
    """
    List all migration revisions with their descriptions and ID.
    """
    revision_app.run()


@app.command()
def go(migration_id: str = typer.Argument(help="Migration ID")):
    """
    Go back (and forward) to specific migration.
    """
    SQLite3Config("cli_test.db")

    manager = RevisionManager()
    revision = manager.get_revision_by_id(int(migration_id))
    print()
    confirmation: str = typer.prompt(
        Fore.RED
        + "THIS OPERATION WILL DELETE ALL DATA IN THE DATABASE.\nARE YOU SURE YOU WANT TO CONTINUE? (y/n)"
    )
    if confirmation.lower() == "y":
        manager.go_to_revision(revision)
    return


@app.command()
def studio(
    schema_file: Union[str, None] = typer.Option(
        None, "--schema-file", "-s", help="Schema file path"
    )
):
    """
    Run web UI for CRUD operations on current DB.
    """
    if schema_file is not None:
        run_server(schema_file=schema_file)
        return

    try:
        schema_file = find_schema_file()
        run_server(schema_file=schema_file)
    except MultipleSchemaFilesError:
        print(
            Fore.RED
            + "Multiple schema files found. Please specify the schema file to use: --schema-file <PATH>"
        )
        raise typer.Exit(code=1)


def main():
    app()


if __name__ == "__main__":
    app()
