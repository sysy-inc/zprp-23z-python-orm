from abc import ABC, abstractmethod


class BaseSQLExecutor(ABC):

    @staticmethod
    @abstractmethod
    def execute_sql(sql: str) -> None:
        """Execute the given SQL query in the database"""
        pass
