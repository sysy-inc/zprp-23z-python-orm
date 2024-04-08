# This file can by run by executing `skibidi-orm` in the terminal, after the package is installed.
# `skibidi-orm migrate [--message <STRING>]`
# `skibidi-orm list-migrations`
# `skibidi-orm go <MIGRATION_ID>`


import typer

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

    if not message:
        message = typer.prompt("Please enter a message for the migration:")

    print(f"Running migration with message: {message}")
    pass


@app.command(name="list-migrations")
def migrate_list():
    """
    List all made migrations with their descriptions and ID.
    """
    print("Listing all migrations")
    pass


@app.command()
def go(migration_id: str = typer.Argument(..., help="Migration ID")):
    """
    Go back (and forward) to specific migration.
    """

    if not migration_id:
        migration_id = typer.prompt("Please enter the migration ID:")

    print(f"Going to migration with ID: {migration_id}")
    pass


def main():
    app()


if __name__ == "__main__":
    app()
