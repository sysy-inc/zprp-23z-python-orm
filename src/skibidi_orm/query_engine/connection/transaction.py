"""
Transactions
"""
from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.operations.crud import Insert
from typing import Any

class Transaction:
    def __init__(self, compiler: SQLCompiler, connection: Any) -> None:
        self._compiler = compiler
        self._conn = connection
        self._insert: list[Insert] = []

    def register_insert(self, obj: Model):
        self._insert.append(Insert(obj))

    def execute(self):
        for insert in self._insert:
            self.execute_insert(insert)

    def execute_insert(self, statement: Insert):
        sql = self._compiler.insert(statement)
        cur = self._conn.cursor()
        cur.execute(sql)
        if statement.returns:
            row = cur.fetchone()
            print(row)
