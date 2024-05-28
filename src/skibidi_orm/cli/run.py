# This file can by run by executing `skibidi-orm` in the terminal, after the package is installed.
# `skibidi-orm migrate [--message <STRING>]`
# `skibidi-orm list-migrations`
# `skibidi-orm go <MIGRATION_ID>`


import typer
from typing import Union
import os

# import shutil
import sys
from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)

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


@app.command(name="list-migrations")
def migrate_list():
    """
    List all made migrations with their descriptions and ID.
    """
    print("Listing all migrations")
    pass


@app.command()
def go(migration_id: Union[str, None] = typer.Argument(None, help="Migration ID")):
    """
    Go back (and forward) to specific migration.
    """

    if migration_id is None:
        migration_id = typer.prompt("Please enter the migration ID:")

    print(f"Going to migration with ID: {migration_id}")
    pass


def main():
    app()


if __name__ == "__main__":
    app()
