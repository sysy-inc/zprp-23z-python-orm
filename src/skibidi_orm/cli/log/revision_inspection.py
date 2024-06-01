from typing import Any
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.containers import Window, DynamicContainer

from skibidi_orm.cli.log.tree import FoldableTree, setup_tree
from skibidi_orm.migration_engine.adapters.base_adapter import BaseTable
from skibidi_orm.migration_engine.adapters.providers import DatabaseProvider
from skibidi_orm.migration_engine.revisions.revision import Revision
from skibidi_orm.migration_engine.adapters.sqlite3_typing import SQLite3Typing


kb = KeyBindings()
revisions: list[Revision] = []


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
main_tree: FoldableTree = FoldableTree(0, "", None, [])
selected_tree: FoldableTree = FoldableTree(0, "", None, [])
expanded_revisions: set[int] = set()
expanded_tables: set[tuple[int, int]] = set()


def get_display_text() -> str:
    """Generate the display text for the application based on the current state."""
    display: list[str] = []
    for child in main_tree.children:
        display.append(str(child))

    return "\n".join(display)


@kb.add("down")
@kb.add("j")
def move_down(_: Any):
    """Move the cursor down the list."""
    global selected_tree
    selected_tree.unselect()
    selected_tree = selected_tree.next()
    selected_tree.select()


@kb.add("up")
@kb.add("k")
def move_up(_: Any):
    """Move the cursor up the list."""
    global selected_tree
    selected_tree.unselect()
    selected_tree = selected_tree.previous()
    selected_tree.select()


@kb.add("h")
@kb.add("left")
def collapse_item(_: Any):
    """Collapse the current item (column list if viewing columns, table list if viewing tables, or the revision if viewing tables)."""
    global selected_tree
    selected_tree.fold()


@kb.add("l")
@kb.add("right")
def expand_item(_: Any):
    """Expand the current item (table list if viewing revisions, column list if viewing tables)."""
    global selected_tree
    selected_tree.unfold()


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


def run_revision_app(revision_list: list[Revision]):
    """Main entry point for the revision inspection app."""
    global revisions
    global main_tree
    global selected_tree

    main_tree, selected_tree = setup_tree(revisions)

    # revisions = revision_list
    revision_app.run()
