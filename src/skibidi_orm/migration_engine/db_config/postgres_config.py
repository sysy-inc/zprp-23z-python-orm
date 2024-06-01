import psycopg2
from skibidi_orm.exceptions.config_exceptions import DbConnectionError
from skibidi_orm.migration_engine.adapters.providers import DatabaseProvider
from skibidi_orm.migration_engine.db_config.base_config import (
    BaseDbConfig,
)
from psycopg2.extensions import connection as Connection


class PostgresConfig(BaseDbConfig):

    database_provider = DatabaseProvider.POSTGRESQL

    """
    Configuration class for Postgres database.
    Instantiating it means choosing Postgres as the database.
    """

    def __init__(
        self, db_name: str, db_user: str, db_password: str, db_host: str, db_port: int
    ):
        self.__db_name = db_name
        self.__db_user = db_user
        self.__db_password = db_password
        self.__db_host = db_host
        self.__db_port = db_port
        self.__connection = self.__create_connection()

    @property
    def db_name(self) -> str:
        return self.__db_name

    @property
    def db_user(self) -> str:
        return self.__db_user

    @property
    def db_password(self) -> str:
        return self.__db_password

    @property
    def db_host(self) -> str:
        return self.__db_host

    @property
    def db_port(self) -> int:
        return self.__db_port

    @property
    def connection(self) -> Connection:
        return self.__connection

    def __create_connection(self) -> Connection:
        try:
            connection = psycopg2.connect(
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name,
            )
        except psycopg2.OperationalError as e:
            raise DbConnectionError(e)

        return connection
