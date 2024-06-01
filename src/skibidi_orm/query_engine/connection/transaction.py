"""
The transaction module provides the Transaction class, which manages database transactions
for executing multiple database operations atomically.
"""
from skibidi_orm.query_engine.adapter.base_compiler import SQLCompiler
from skibidi_orm.query_engine.model.base import Model
from skibidi_orm.query_engine.operations.crud import Insert, Update, Delete
from typing import Any


class Transaction:
    """
    Manages a transaction for executing multiple database operations.

    Attributes:
        _compiler (SQLCompiler): The SQL compiler used to generate SQL statements.
        _conn (Any): The connection object to the database.
        _insert (list[Insert]): A list of Insert statements to be executed.
        _update (list[Update]): A list of Update statements to be executed.
        _delete (list[Delete]): A list of Delete statements to be executed.
    """
    def __init__(self, compiler: SQLCompiler, connection: Any) -> None:
        """
        Initializes a Transaction object.

        Args:
            compiler (SQLCompiler): The SQL compiler used to generate SQL statements.
            connection (Any): The connection object to the database.
        """
        self._compiler = compiler
        self._conn = connection
        self._insert: list[Insert] = []
        self._update: list[Update] = []
        self._delete: list[Delete] = []

    @property
    def insert_list(self):
        """
        Returns the list of Insert statements in the transaction.

        Returns:
            list[Insert]: A list of Insert statements.
        """
        return self._insert

    @property
    def update_list(self):
        """
        Returns the list of Update statements in the transaction.

        Returns:
            list[Update]: A list of Update statements.
        """
        return self._update

    @property
    def delete_list(self):
        """
        Returns the list of Delete statements in the transaction.

        Returns:
            list[Delete]: A list of Delete statements.
        """
        return self._delete

    def register_insert(self, obj: Model):
        """
        Registers an Insert statement for the given model object.

        Args:
            obj (Model): The model object for which to register an Insert statement.
        """
        self._insert.append(Insert(obj))

    def register_update(self, obj: Model):
        """
        Registers an Update statement for the given model object.

        Args:
            obj (Model): The model object for which to register an Update statement.
        """
        self._update.append(Update(obj))

    def register_delete(self, obj: Model):
        """
        Registers a Delete statement for the given model object.

        Args:
            obj (Model): The model object for which to register a Delete statement.
        """
        self._delete.append(Delete(obj))

    def execute(self):
        """
        Executes all registered Insert, Update, and Delete statements in the transaction.
        """
        for insert in self._insert:
            self.execute_insert(insert)
        for update in self._update:
            self.execute_update(update)
        for delete in self._delete:
            self.execute_delete(delete)

    def execute_insert(self, statement: Insert):
        """
        Executes the given Insert statement.

        Args:
            statement (Insert): The Insert statement to execute.
        """
        sql = self._compiler.insert(statement)
        cur = self._conn.cursor()
        cur.execute(sql)
        if statement.returns:
            row = cur.fetchone()
            statement._obj.pk = row[0]     # type: ignore

    def execute_update(self, statement: Update):
        """
        Executes the given Update statement.

        Args:
            statement (Update): The Update statement to execute.
        """
        sql = self._compiler.update(statement)
        cur = self._conn.cursor()
        cur.execute(sql)

    def execute_delete(self, statement: Delete):
        """
        Executes the given Delete statement.

        Args:
            statement (Delete): The Delete statement to execute.
        """
        sql = self._compiler.delete(statement)
        cur = self._conn.cursor()
        cur.execute(sql)
