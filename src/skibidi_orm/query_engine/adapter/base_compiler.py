"""
Base sql compiler
"""
from skibidi_orm.query_engine.operations.crud import Insert, ValueBase, Update, Delete
from skibidi_orm.query_engine.operations import clauses as c
from skibidi_orm.query_engine.operations.select import Select
from skibidi_orm.query_engine.operations.functions import Function, Count
from typing import Any, Type


class SQLCompiler:
    CLAUSES: dict[Type[c.Clause], str] = {
        c.Eq: "=",
        c.Gt: ">",
        c.GtEq: ">=",
        c.Lt: "<",
        c.LtEq: "<=",
        c.NotEq: "!=",
        c.NotNull: " IS NOT NULL",
        c.Null: " IS NULL"
    }

    FUNCTIONS: dict[Type[Function], str] = {
        Count: "COUNT"
    }

    def _prepare_columns(self, statement: ValueBase) -> str:
        columns = statement.columns()
        text = ', '.join(columns)
        return text

    def _prep_val(self, val: Any):
        text = ""
        if val:
            text = f"'{val}'" if isinstance(val, str) else str(val)
        return text

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

    def _prepare_where(self, clauses: tuple[c.Clause, ...]):
        text = "WHERE "
        for clause in clauses:
            text += f"{clause.col}{self.CLAUSES.get(clause.type)}{self._prep_val(clause.val)}"
            text += " AND "
        return text[:-5]

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

    def delete(self, statement: Delete) -> str:
        text = "DELETE FROM "
        text += statement.table()
        text += " "
        text += self._prepare_where(statement.where_clause())
        text += ";"
        print(text)
        return text
    
    def _agregate_function(self, func: Function):
        text = f"{self.FUNCTIONS[func.type]}({func.column})"
        return text
    
    def _alias(self, alias: str):
        text = f" AS {alias}"
        return text
    
    def _select_columns(self, statement: Select):
        fields = statement.fields
        text = ""
        for field in fields:
            # check if agregate function
            if isinstance(field, Function):
                text += self._agregate_function(field)
            # just column name
            else:
                text += field

            if field in statement.annotations:
                # there is an alias to be made
                text += self._alias(statement.annotations[field])

            text += ", "
        return text[:-2]
    
    def select(self, statement: Select) -> str:
        text = "SELECT "
        text += self._select_columns(statement)
        text += " "
        text += f"FROM {statement.table} "
        # WHERE
        if statement.where_clauses:
            text += self._prepare_where(tuple(statement.where_clauses))
            text += " "
        # GROUP BY
        if statement.group_by_col:
            text += "GROUP BY "
            text += ", ".join(statement.group_by_col)
            text += " "
        # ORDERE BY
        if statement.order_by_col[0]:
            text += "ORDER BY "
            text += ", ".join(statement.order_by_col[0])
            if statement.order_by_col[1]:
                # it is descend
                text += " DESC"
            text += " "
        text += ";"
        print(text)
        return text
