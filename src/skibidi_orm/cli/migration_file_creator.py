import os
from skibidi_orm.migration_engine.adapters.database_objects.migration_element import (
    MigrationElement,
)


def create_migration_file(migration_element: MigrationElement):
    """
    Inspect a migration element and create a Python file that can be executed to apply the migration.
    """
    migration_file_path = os.path.join(*[os.getcwd(), "migrations", "migration.py"])

    migration_element.migrate(preview=True)

    operations = migration_element.operations

    # with open(migration_file, "w") as f:
    #     f.write("# This is an auto-generated migration file.\n")
    #     f.write("# Do not modify this file directly.\n")
    #     f.write("\n")
    #     f.write("from skibidi_orm.migration_engine.studio import MigrationStudio\n")
    #     f.write("\n")
    #     f.write("\n")
    #     f.write(f"def apply_migration(migration_studio: MigrationStudio):\n")
    #     f.write("    # Begin migration\n")
    #     f.write("\n")

    #     for operation in migration_element.operations:
    #         f.write(f"    {operation}\n")

    #     f.write("\n")
    #     f.write("    # End migration\n")
    #     f.write("\n")
    #     f.write("\n")
    #     f.write("if __name__ == '__main__':\n")
    #     f.write("    migration_studio = MigrationStudio()\n")
    #     f.write("    apply_migration(migration_studio)\n")

    # print(f"Migration file created: {migration_file}")
    # print("To apply the migration, run the following command:")
    # print(f"python {migration_file}")
    # print("\n")
