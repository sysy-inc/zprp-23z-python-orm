import pytest
from skibidi_orm.exceptions.config_exceptions import DbConnectionError
from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig
from psycopg2.extensions import connection as Connection


def test_create_connection_valid():
    """
    Should connect to running Postgres database.
    Make sure to have a running Postgres database.
    """
    config = PostgresConfig(
        db_name="postgres",
        db_user="admin",
        db_password="admin",
        db_host="0.0.0.0",
        db_port=5432,
    )
    assert config.connection is not None
    assert isinstance(config.connection, Connection)
    assert config.connection.closed == 0
    config.connection.close()
    assert config.connection.closed == 1


@pytest.mark.slow
@pytest.mark.parametrize(
    "db_name, db_user, db_password, db_host, db_port",
    [
        ("invalid", "admin", "admin", "admin", 5432),
        ("postgres", "invalid", "admin", "admin", 5432),
        ("postgres", "admin", "invalid", "admin", 5432),
        ("postgres", "admin", "admin", "invalid", 5432),
        ("postgres", "admin", "admin", "admin", 1337),
    ],
)
def test_should_raise_DbConnectionError_on_invalid_connection(
    db_name, db_user, db_password, db_host, db_port  # type: ignore
):
    with pytest.raises(DbConnectionError):
        PostgresConfig(
            db_name=db_name,  # type: ignore
            db_user=db_user,  # type: ignore
            db_password=db_password,  # type: ignore
            db_host=db_host,  # type: ignore
            db_port=db_port,  # type: ignore
        )
