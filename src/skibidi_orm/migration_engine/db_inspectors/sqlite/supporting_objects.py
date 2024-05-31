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
        # todo: better typing?
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
