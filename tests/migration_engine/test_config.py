import pytest
from skibidi_orm.migration_engine.config import PostgresConfig, SQLite3Config


def test_should_only_create_one_instance_of_each_config():
    x = SQLite3Config(db_path="first_path")
    y = SQLite3Config(db_path="next_path")
    assert x is y
    assert x.db_path == "first_path"
    assert y.db_path == "first_path"


def test_should_raise_error_when_instantiating_other_config():
    SQLite3Config(db_path="first_path")
    with pytest.raises(RuntimeError) as exc_info:
        PostgresConfig(db_path="first_path")
    assert str(exc_info.value) == "Only one instance of this class is allowed"


def test_accessing_through_instance_method_should_throw_error_when_instance_does_not_exist():
    with pytest.raises(ReferenceError) as exc_info:
        SQLite3Config.instance()
    assert str(exc_info.value) == "Instance does not exist"