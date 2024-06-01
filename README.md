# zprp-23z-python-orm
* [Migration engine](#migration-engine)
  * [Usage](#usage)
    * [Implementation of `schema.py`](#implementation-of-schemapy)
    * [CLI](#cli)
      * [go](#go)
      * [list-migrations](#list-migrations)
      * [migrate](#migrate)
      * [preview-migration](#preview-migration)
      * [studio](#studio)

# Migration engine
## Installation

```bash
pip install skibidi-orm
```

## Usage

### Implementation of `schema.py`

Primary functionallity of the migration engine is to allow for easy megrations between different versions of the database, so structure of schema file should be defined by proprioetary library using migration engine.

Hovewer we can define example schema file as follows for example purposes:
```python
# schema.py
# ...

class Table(MigrationElement):

    def __init__(self) -> None:
        self.adapter = SQLite3Adapter()

        models = Table.__subclasses__()
        if self.__class__ == Table:
            for cls in models:
                self.adapter.create_table(cls.__dict__["table"])


class Post(Table):
    columns = [
        SQLite3Typing.Column(
            name="post_id",
            data_type="INTEGER",
            column_constraints=[c.PrimaryKeyConstraint("Post", "post_id")],
        ),
        SQLite3Typing.Column(
            name="post_name",
            data_type="TEXT",
            column_constraints=[c.NotNullConstraint("Post", "post_name")],
        ),
    ]

    table = SQLite3Typing.Table(name="Post", columns=columns)


SQLite3Config("test_database.db")
```

Above we defined simple implementation of `Table` class which works as a base model for all SQL tables in our databse.

Normally `Table` class would be abstracted away by proprietary library, but for the sake of example we defined it here.

When he have defined our schema all interactions of end-user with the migration engine are done through CLI.

# `skibidi-orm`

CLI tool for managing schema creations and migrations in Skibidi ORM.

**Usage**:

```console
$ skibidi-orm [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `-s, --schema-file PATH`: Specify an external schema file path
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

**Commands**:

* `go`: Go back (and forward) to specific migration.
* `log`: List all migration revisions with their...
* `migrate`: Used to run migration for current schema...
* `preview-migration`: Preview the migration that will be executed.
* `studio`: Run web UI for CRUD operations on current DB.

## `skibidi-orm go`

Go back (and forward) to specific migration.

**Usage**:

```console
$ skibidi-orm go [OPTIONS] MIGRATION_ID
```

**Arguments**:

* `MIGRATION_ID`: Migration ID  [required]

**Options**:

* `--help`: Show this message and exit.

## `skibidi-orm log`

List all migration revisions with their descriptions and ID.

**Usage**:

```console
$ skibidi-orm log [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `skibidi-orm migrate`

Used to run migration for current schema file. Can accept an optional message as a description of the migration.

**Usage**:

```console
$ skibidi-orm migrate [OPTIONS]
```

**Options**:

* `-m, --message TEXT`: Description of migration
* `-d, --direct`: Use --direct to run the migration directly. Without the flag, it will create a python migration file.
* `--help`: Show this message and exit.

## `skibidi-orm preview-migration`

Preview the migration that will be executed.

**Usage**:

```console
$ skibidi-orm preview-migration [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

## `skibidi-orm studio`

Run web UI for CRUD operations on current DB.

**Usage**:

```console
$ skibidi-orm studio [OPTIONS]
```

**Options**:

* `-s, --schema-file TEXT`: Schema file path
* `--help`: Show this message and exit.
