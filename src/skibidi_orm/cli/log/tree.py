from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Optional, cast

from skibidi_orm.migration_engine.adapters.base_adapter import BaseColumn, BaseTable
from skibidi_orm.migration_engine.revisions.revision import Revision


@dataclass
class Node:
    index: int
    value: str
    parent: Optional[FoldableTree]
    unfolded: bool = field(init=False, default=False)

    def fold(self):
        self.unfolded = False

    def unfold(self):
        self.unfolded = True

    @classmethod
    def from_column(
        cls, index: int, parent: FoldableTree, column: BaseColumn[Any]
    ) -> Leaf:
        """Create a leaf node from a column object."""
        return Leaf.from_column(index, parent, column)

    @classmethod
    def from_table(
        cls, index: int, parent: FoldableTree, table: BaseTable[BaseColumn[Any]]
    ) -> Node:
        """Create a node from a table object. If the table has no columns, return a leaf node.
        Otherwise, return a foldable tree node with leaf nodes as children."""

        if not table.__dict__.get("columns", False):
            return Leaf.from_table(index, parent, table)
        return FoldableTree.from_table(index, parent, table)

    @classmethod
    def from_revision(
        cls, index: int, parent: FoldableTree, revision: Revision
    ) -> Node:
        """Create a foldable tree node from a revision object. Each table in the revision"""
        return FoldableTree.from_revision(index, parent, revision)


@dataclass
class FoldableTree(Node):
    """Class representing a foldable tree structure.
    Used to display the revisions in the log"""

    children: list[Node]
    selected: bool = field(default=False)

    def __str__(self):
        lines = [self.value if not self.selected else f"> {self.value}"]
        if self.unfolded:
            for child in self.children:
                lines.append(f"  {child}")
        return "\n".join(lines)

    def fold(self):
        self.unfolded = False

    def unfold(self):
        self.unfolded = True

    def select(self):
        self.selected = True

    def unselect(self):
        self.selected = False

    @classmethod
    def from_table(
        cls, index: int, parent: FoldableTree, table: BaseTable[BaseColumn[Any]]
    ) -> FoldableTree:
        return_value = cls(index, str(table), parent, [])
        # create a list of children nodes
        nodes: list[Node] = [
            Node.from_column(i, return_value, column)
            for i, column in enumerate(table.columns)
        ]
        # set the children of the root node
        return_value.children = nodes
        return return_value

    @classmethod
    def from_revision(
        cls, index: int, parent: FoldableTree, revision: Revision
    ) -> FoldableTree:
        return_value = cls(index, f"{index + 1}) {revision}", parent, []) # todo
        # create a list of children nodes
        nodes: list[Node] = [
            Node.from_table(i, return_value, table)
            for i, table in enumerate(revision.tables)
        ]
        # set the children of the root node
        return_value.children = nodes
        return return_value

    @classmethod
    def from_revision_list(cls, revisions: list[Revision]) -> FoldableTree:
        """Create a foldable tree structure from a list of revisions.
        This is the root node of the tree used in the app."""

        root = cls(-1, "Revisions", None, [])

        # create a list of children nodes
        nodes: list[Node] = [
            FoldableTree.from_revision(i, root, revision)
            for i, revision in enumerate(revisions)
        ]

        # set the children of the root node
        root.children = nodes
        return root

    def next_sibling(self) -> FoldableTree | None:
        """Return the next sibling of the tree node."""
        if self.parent is None:
            return None
        return self.parent.get_first_tree_child_after(self.index)

    def previous_sibling(self) -> FoldableTree | None:
        """Return the previous sibling of the tree node."""
        if self.parent is None:
            return None
        return self.parent.get_first_tree_child_before(self.index)

    def next(self) -> FoldableTree:
        """Return the next tree node in the tree structure."""
        # if unfolded, try to find some child tree to move to
        if self.parent is None:
            # root node always contains children, so casting is safe
            first_tree_child = cast(FoldableTree, self.get_first_tree_child_after(-1))
            return first_tree_child

        # if unfolded, we want to return the child if there is one
        first_tree_child = self.get_first_tree_child_after(-1)
        # if no child/not unfolded, return the next sibling
        next_sibling = self.next_sibling()
        # if there is no next sibling, return the node after the parent
        next_uncle = self.parent.next_sibling()
        # finally, if there is no next uncle, return the parent's last c

        if first_tree_child is not None:
            return first_tree_child

        elif next_sibling is not None:
            return next_sibling

        if next_uncle is not None:
            return next_uncle

        # we are the last node in the main tree, nowhere to go
        return self

    def previous(self) -> FoldableTree:
        """Return the previous tree node in the tree structure."""
        if self.parent is None:
            # if we are the root node, we want to return the last child
            # the root always contains children, so casting is safe
            last_child = cast(FoldableTree, self.children[-1])
            return last_child

        # try to find the previous sibling
        previous_sibling = self.previous_sibling()
        if previous_sibling is not None:
            if previous_sibling.unfolded:
                last_child = previous_sibling.get_first_tree_child_before(
                    len(previous_sibling.children)
                )
                if last_child is not None:
                    return last_child
            return previous_sibling

        # edge case - the parent is the root node, and we are the first child - nowhere to go
        if self.parent.parent is None:
            return self

        # in any other case, return the parent
        return self.parent

    def get_first_tree_child_after(self, index: int) -> FoldableTree | None:
        """Return the first tree node after the given index."""
        if not self.children or not self.unfolded:
            return None

        for i in range(index + 1, len(self.children)):
            if isinstance(self.children[i], FoldableTree):
                return cast(FoldableTree, self.children[i])
        return None

    def get_first_tree_child_before(self, index: int) -> FoldableTree | None:
        """Return the first tree node before the given index."""
        if not self.children or not self.unfolded:
            return None

        for i in range(index - 1, -1, -1):
            if isinstance(self.children[i], FoldableTree):
                return cast(FoldableTree, self.children[i])
        return None


@dataclass
class Leaf(Node):
    """Class representing a leaf in a tree structure.
    A leaf is not selectable and does not have children nodes."""

    def __str__(self):
        return f"  {self.value}"

    @classmethod
    def from_column(
        cls, index: int, parent: FoldableTree, column: BaseColumn[Any]
    ) -> Leaf:
        return cls(index, str(column), parent)

    @classmethod
    def from_table(
        cls, index: int, parent: FoldableTree, table: BaseTable[BaseColumn[Any]]
    ) -> Leaf:
        return cls(index, str(table), parent)


def setup_tree(revisions: list[Revision]) -> tuple[FoldableTree, FoldableTree]:
    """Create a foldable tree structure from a list of revisions.
    Returns the main tree and the tree to be first selected on the screen"""
    tree = FoldableTree.from_revision_list(revisions)
    tree.unfold()
    first_child = cast(FoldableTree, tree.children[0])
    first_child.select()
    return tree, first_child
