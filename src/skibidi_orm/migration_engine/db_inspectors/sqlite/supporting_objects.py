from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Any


@dataclass(frozen=True)
class PragmaTableInfoEntry:
    cid: int
    name: str
    data_type: str
    notnull: Literal[0, 1]
    dflt_value: Any
    pk: Literal[0, 1]

    @classmethod
    def from_tuple(
        cls,
        values: tuple[int, str, str, Literal[0, 1], Any, Literal[0, 1]],
    ) -> PragmaTableInfoEntry:
        cid, name, type, notnull, dflt_value, pk = values
        return cls(int(cid), name, type, notnull, dflt_value, pk)


@dataclass(frozen=True)
class PragmaForeignKeyListEntry:
    id: int
    seq: int
    table: str
    from_column: str
    to_column: str
    on_update: str
    on_delete: str
    match: str

    @classmethod
    def from_tuple(
        cls,
        values: tuple[str, str, str, str, str, str, str, str],
    ) -> PragmaForeignKeyListEntry:
        id, seq, table, from_column, to_column, on_update, on_delete, match = values
        return cls(
            int(id),
            int(seq),
            table,
            from_column,
            to_column,
            on_update,
            on_delete,
            match,
        )


@dataclass(frozen=True)
class PragmaIndexListEntry:
    id: int
    name: str
    unique: Literal[0, 1]
    creation_method: Literal["c", "u", "pk"]
    partial: Literal[0, 1]

    @classmethod
    def from_tuple(
        cls,
        values: tuple[int, str, Literal[0, 1], Literal["c", "u", "pk"], Literal[0, 1]],
    ) -> PragmaIndexListEntry:
        id, name, unique, creation_method, partial = values
        return cls(int(id), name, unique, creation_method, partial)


@dataclass(frozen=True)
class PragmaIndexInfoEntry:
    """Class representing the information about a column's
    role in an index. From the SQLite3 docs:
    This pragma returns one row for each key column in the named index.
    A key column is a column that is actually named in the CREATE INDEX
    index statement or UNIQUE constraint or PRIMARY KEY constraint that
    created the index. Index entries also usually contain auxiliary columns
    that point back to the table row being indexed. The auxiliary index-columns
    are not shown by the index_info pragma, but they are listed by the index_xinfo pragma.

    Output columns from the index_info pragma are as follows:

    The rank of the column within the index. (0 means left-most.)
    The rank of the column within the table being indexed.
    The name of the column being indexed. This columns is NULL if the column is the rowid or an expression.
    """

    column_rank_within_index: int
    column_rank_wihtin_table: int
    column_name: str | None

    @classmethod
    def from_tuple(
        cls,
        values: tuple[int, int, str],
    ) -> PragmaIndexInfoEntry:
        column_rank_within_index, column_rank_wihtin_table, column_name = values
        return cls(column_rank_within_index, column_rank_wihtin_table, column_name)
