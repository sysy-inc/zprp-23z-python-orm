"""
Base sql compiler
"""
from skibidi_orm.query_engine.operations.crud import Insert, ValueBase, Update
from skibidi_orm.query_engine.operations import clauses as c
from typing import Any, Type


class SQLCompiler:
    CLAUSES: dict[Type[c.Clause], str] = {
        c.Eq: "="
    }

    def _prepare_columns(self, statement: ValueBase) -> str:
        columns = statement.columns()
        text = ', '.join(columns)
        return text

    def _prep_val(self, val: Any):
        return f"'{val}'" if isinstance(val, str) else str(val)

    def _prepare_values(self, statement: ValueBase) -> str:
        val = statement.values()
        processed_values = [
            self._prep_val(v)
            for v in val
        ]
        text = ', '.join(processed_values)
        return text

    def _prepare_returning(self, columns: list[Any]) -> str:
        if len(columns) == 1:
            return f"RETURNING {columns[0]}"
        else:
            return "RETURNING " + ", ".join(columns)

    def insert(self, statement: Insert) -> str:
        text = "INSERT INTO "
        text += statement.table()
        text += " ("
        text += self._prepare_columns(statement)
        text += ") "
        text += "VALUES "
        text += "("
        text += self._prepare_values(statement)
        text += ")"
        if statement.returns:
            text += self._prepare_returning(statement.returning_col)
        text += ";"
        print(text)
        return text

    def _col_val(self, attributes: list[tuple[str, Any]]) -> str:
        text = ""
        for col, val in attributes:
            text += f'{col}={self._prep_val(val)}, '
        return text[:-2]

    def _prepare_where(self, clauses: tuple[c.Clause]):
        text = "WHERE "
        for clause in clauses:
            text += f"{clause.col}{self.CLAUSES.get(clause.type)}{self._prep_val(clause.val)}, "
        return text[:-2]

    def update(self, statement: Update) -> str:
        text = "UPDATE "
        text += statement.table()
        text += " SET "
        text += self._col_val(statement.attributes())
        text += " "
        text += self._prepare_where(statement.where_clause())
        text += ";"
        print(text)
        return text
