"""
Transactions
"""
from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.operations.crud import Insert, Update
from typing import Any


class Transaction:
    def __init__(self, compiler: SQLCompiler, connection: Any) -> None:
        self._compiler = compiler
        self._conn = connection
        self._insert: list[Insert] = []
        self._update: list[Update] = []

    def register_insert(self, obj: Model):
        self._insert.append(Insert(obj))

    def register_update(self, obj: Model):
        self._update.append(Update(obj))

    def execute(self):
        for insert in self._insert:
            self.execute_insert(insert)
        for update in self._update:
            self.execute_update(update)

    def execute_insert(self, statement: Insert):
        sql = self._compiler.insert(statement)
        cur = self._conn.cursor()
        cur.execute(sql)
        if statement.returns:
            row = cur.fetchone()
            print(row)

    def execute_update(self, statement: Update):
        sql = self._compiler.update(statement)
        cur = self._conn.cursor()
        cur.execute(sql)
