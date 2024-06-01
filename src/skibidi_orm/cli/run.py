# This file can by run by executing `skibidi-orm` in the terminal, after the package is installed.
# `skibidi-orm migrate [--message <STRING>]`
# `skibidi-orm list-migrations`
# `skibidi-orm go <MIGRATION_ID>`


from pathlib import Path
import typer
from typing import Union, Any
import os

# import shutil
import sys
from skibidi_orm.cli.migration_file_creator import create_migration_file
from skibidi_orm.cli.utils import find_schema_file, load_schema_from_path
from skibidi_orm.exceptions.cli_exceptions import MultipleSchemaFilesError
from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable
from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)
from skibidi_orm.migration_engine.db_config.base_config import BaseDbConfig
from skibidi_orm.migration_engine.revisions.manager import RevisionManager
from skibidi_orm.migration_engine.revisions.revision import Revision
from skibidi_orm.migration_engine.studio.server import run_server
from skibidi_orm.cli.log.revision_inspection import run_revision_app  # type: ignore
from colorama import Fore

sys.path.insert(0, os.getcwd())


app = typer.Typer(
    help="CLI tool for managing schema creations and migrations in Skibidi ORM."
)
state = {"schema_path": Path()}


@app.callback()
def schema_callback(
    schema_path: Union[None, Path] = typer.Option(
        None,
        "--schema-file",
        "-s",
        help="Specify an external schema file path",
        show_default=False,
    )
):
    """
    Specify a path to the schema file to use.
    """

    if schema_path is not None:
        state["schema_path"] = schema_path

        try:
            load_schema_from_path(str(schema_path))
            print("\nSchema file successfully loaded.\n")

        except FileNotFoundError:
            print("\nSchema file could not be found. Aborting.\n")
            raise typer.Exit(code=1)

        except ImportError:
            print("\nSchema file could not be loaded. Aborting.\n")
            raise typer.Exit(code=1)

    else:
        try:
            import schema as schema  # type: ignore

            print("\nSchema file successfully loaded.\n")

        except ImportError:
            print("\nSchema file could not be loaded. Aborting.\n")
            raise typer.Exit(code=1)


@app.command()
def migrate(
    message: str = typer.Option(
        None,
        "--message",
        "-m",
        help="Description of migration",
    ),
    direct: bool = typer.Option(
        False,
        "--direct",
        "-d",
        help="Use --direct to run the migration directly. Without the flag, it will create a python migration file.",
    ),
):
    """
    Used to run migration for current schema file. Can accept an optional message as a description of the migration.
    """
    m = MigrationElement()
    if direct:
        m.migrate(preview=False)
        tables: list[BaseTable[Any]] = m.adapter.tables  # type: ignore todo
        manager = RevisionManager()
        revision = Revision(
            "No message provided" if message is None else message,  # type: ignore
            "",  # this field is deprecated and to be removed in future versions
            BaseDbConfig.get_instance().database_provider,
            tables,  # type: ignore todo
        )
        manager.save_revision(revision)
        print("\nMigration complete. \n")
    else:
        create_migration_file(m)
        print("\nMigration file created. \n")
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
        print("Migration preview:")
        for i, operation in enumerate(m.operations):
            print(f"\t{i+1}) {operation}")
    pass


@app.command(name="log")
def migrate_list():
    """
    List all migration revisions with their descriptions and ID.
    """
    manager = RevisionManager()
    revisions = manager.get_all_revisions()

    if not revisions:
        print("No revisions found.")
        return

    run_revision_app(list(revisions.values()))


@app.command(name="go")
def go(migration_id: str = typer.Argument(help="Migration ID")):
    """
    Go back (and forward) to specific migration.
    """

    manager = RevisionManager()
    revision = manager.get_revision_by_id(int(migration_id))
    print()
    confirmation: str = typer.prompt(
        Fore.RED
        + "THIS OPERATION WILL DELETE ALL DATA IN THE DATABASE.\nARE YOU SURE YOU WANT TO CONTINUE? (y/n)"
    )
    if confirmation.lower() == "y":
        manager.go_to_revision(revision)
        print(Fore.GREEN + "Operation complete.")
    else:
        print(Fore.RED + "Operation aborted.")


@app.command()
def studio(
    schema_file: Union[str, None] = typer.Option(
        None, "--schema-file", "-s", help="Schema file path"
    )
):
    """
    Run web UI for CRUD operations on current DB.
    """

    try:
        if schema_file is None:
            schema_file = find_schema_file()
    except MultipleSchemaFilesError:
        print(
            Fore.RED
            + "Multiple schema files found. Please specify the schema file to use: --schema-file <PATH>"
        )
        raise typer.Exit(code=1)

    try:
        run_server(schema_file=schema_file)
    except Exception as e:
        print(Fore.RED + f"Error: {e}")
        raise typer.Exit(code=1)


def main():
    app()


if __name__ == "__main__":
    app()
