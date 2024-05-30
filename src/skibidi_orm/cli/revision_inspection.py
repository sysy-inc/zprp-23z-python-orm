from typing import Any
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window, DynamicContainer

from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable
from skibidi_orm.migration_engine.adapters.providers import DatabaseProvider
from skibidi_orm.migration_engine.revisions.revision import Revision
from skibidi_orm.migration_engine.adapters.sqlite3_typing import SQLite3Typing

kb = KeyBindings()


# Sample data for demonstration
revisions = [
    Revision(
        description="Initial migration",
        schema_repr="Schema v1",
        provider=DatabaseProvider.SQLITE3,
        tables=[
            SQLite3Typing.Table(
                name="Users",
                columns=[
                    SQLite3Typing.Column("id", "INTEGER"),
                    SQLite3Typing.Column("name", "TEXT"),
                ],
            ),
            BaseTable(
                name="Orders",
                columns=[
                    SQLite3Typing.Column("id", "INTEGER"),
                    SQLite3Typing.Column("user_id", "INTEGER"),
                    SQLite3Typing.Column("amount", "REAL"),
                ],
            ),
        ],
    ),
    Revision(
        description="Added products table",
        schema_repr="Schema v2",
        provider=DatabaseProvider.SQLITE3,
        tables=[
            BaseTable(
                name="Products",
                columns=[
                    SQLite3Typing.Column("id", "INTEGER"),
                    SQLite3Typing.Column("name", "TEXT"),
                    SQLite3Typing.Column("price", "REAL"),
                ],
            )
        ],
    ),
]


# Current position and expanded states
current_index = 0
expanded_revisions: set[int] = set()
expanded_tables: set[tuple[int, int]] = set()


def get_display_text() -> str:
    """Generate the display text for the application based on the current state."""
    display: list[str] = []
    index = 0
    for rev_index, revision in enumerate(revisions):
        # Add revision to display
        display.append(f"{'> ' if index == current_index else '  '}{revision}")
        index += 1
        if rev_index in expanded_revisions:
            for table_index, table in enumerate(revision.tables):
                # Add table to display
                display.append(
                    f"{'    > ' if index == current_index else '      '}{table}"
                )
                index += 1
                if (rev_index, table_index) in expanded_tables:
                    for column in table.columns:
                        # Add column to display
                        display.append(
                            f"{'        > ' if index == current_index else '        '}{column}"
                        )
                        index += 1
    return "\n".join(display)


def calculate_max_index() -> int:
    """Calculate the maximum index based on the current state of expanded revisions and tables."""
    index = 0
    for rev_index, revision in enumerate(revisions):
        index += 1
        if rev_index in expanded_revisions:
            for table_index, table in enumerate(revision.tables):
                index += 1
                if (rev_index, table_index) in expanded_tables:
                    index += len(table.columns)
    return index


@kb.add("down")
@kb.add("j")
def move_down(event: Any):
    """Move the cursor down the list."""
    global current_index
    current_index = (current_index + 1) % calculate_max_index()


@kb.add("up")
@kb.add("k")
def move_up(event: Any):
    """Move the cursor up the list."""
    global current_index
    current_index = (
        current_index - 1 if current_index != 0 else calculate_max_index() - 1
    )


@kb.add("h")
@kb.add("left")
def collapse_item(event: Any):
    """Collapse the current item (column list if viewing columns, table list if viewing tables, or the revision if viewing tables)."""
    global current_index, expanded_revisions, expanded_tables
    index = 0
    for rev_index, revision in enumerate(revisions):
        if index == current_index:
            if rev_index in expanded_revisions:
                expanded_revisions.discard(rev_index)
            return
        index += 1
        if rev_index in expanded_revisions:
            for table_index, table in enumerate(revision.tables):
                if index == current_index:
                    if (rev_index, table_index) in expanded_tables:
                        expanded_tables.discard((rev_index, table_index))
                    return
                index += 1
                if (rev_index, table_index) in expanded_tables:
                    index += len(table.columns)


@kb.add("l")
@kb.add("right")
def expand_item(event: Any):
    """Expand the current item (table list if viewing revisions, column list if viewing tables)."""
    global current_index, expanded_revisions, expanded_tables
    index = 0
    for rev_index, revision in enumerate(revisions):
        if index == current_index:
            expanded_revisions.add(rev_index)
            return
        index += 1
        if rev_index in expanded_revisions:
            for table_index, table in enumerate(revision.tables):
                if index == current_index:
                    expanded_tables.add((rev_index, table_index))
                    return
                index += 1
                if (rev_index, table_index) in expanded_tables:
                    index += len(table.columns)


@kb.add("q")
def exit_app(event: Any):
    """Exit the application."""
    event.app.exit()


# Dynamic container for updating the display
body = DynamicContainer(
    lambda: Window(FormattedTextControl(get_display_text()), wrap_lines=True)
)
root_container = HSplit([body])
layout = Layout(root_container)

# Create and run the application
revision_app = Application(layout=layout, key_bindings=kb, full_screen=True)  # type: ignore
