"""
Base sql compiler
"""
from skibidi_orm.query_engine.operations.crud import Insert, ValueBase
from typing import Any

class SQLCompiler:

    def _prepare_columns(self, statement: ValueBase) -> str:
        columns = statement.columns()
        text = ', '.join(columns)
        return text
    
    def _prepare_values(self, statement: ValueBase) -> str:
        val = statement.values()
        processed_values = [
            f"'{v}'" if isinstance(v, str) else str(v)
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
