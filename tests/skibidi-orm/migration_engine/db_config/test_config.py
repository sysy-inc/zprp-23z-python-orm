import pytest
from skibidi_orm.migration_engine.db_config.postgres_config import PostgresConfig
from skibidi_orm.migration_engine.db_config.sqlite3_config import SQLite3Config
import os


def test_should_raise_error_on_invalid_insantiation():
    """
    We cannot instantiate more than one config
    """
    with pytest.raises(RuntimeError) as exc_info:
        SQLite3Config(db_path="first_path")
        SQLite3Config(db_path="next_path")
    assert str(exc_info.value) == "Only one instance of this class is allowed"


def test_should_raise_error_when_instantiating_other_config():
    """
    Should raise error when trying to instantiate other config after one has been instantiated
    """
    SQLite3Config(db_path="first_path")
    with pytest.raises(RuntimeError) as exc_info:
        PostgresConfig(
            db_name="db_name",
            db_user="db_user",
            db_password="db_password",
            db_host="db_host",
            db_port=5432,
        )
    assert str(exc_info.value) == "Only one instance of this class is allowed"


def test_accessing_through_instance_method_should_throw_error_when_instance_does_not_exist():
    """
    Should raise error when trying to access instance method when instance does not exist
    """
    with pytest.raises(ReferenceError) as exc_info:
        SQLite3Config.get_instance()
    assert str(exc_info.value) == "Instance does not exist"


def test_check_argument_saving():
    """
    Should raise error when arguments are not saved
    """
    config = SQLite3Config(db_path="first_path")
    assert config.db_path == os.path.join(os.getcwd(), "first_path")
