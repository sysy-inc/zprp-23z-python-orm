from skibidi_orm.query_engine.model.meta_options import MetaOptions
import pytest


@pytest.fixture
def meta_options() -> MetaOptions:
    meta_attrs = {'db_table': 'test_table'}
    return MetaOptions(meta_attrs)

def test_meta_options_init(meta_options: MetaOptions):
    assert meta_options.db_table == 'test_table'
    assert meta_options.meta == {'db_table': 'test_table'}
    assert meta_options.primary_key is None
    assert meta_options.local_fields == []


def test_meta_options_contribute_to_class(meta_options: MetaOptions):
    class TestClass:
        pass
    meta_options.contribute_to_class(TestClass, 'meta')
    assert hasattr(TestClass, '_meta')
    assert hasattr(meta_options, 'model')

def test_meta_option_add_field(meta_options: MetaOptions):
    pass

def test_setup_pk_first_primary_key(meta_options: MetaOptions):
    class Field:
        primary_key = True
    field = Field
    meta_options.setup_pk(field)
    assert meta_options.primary_key == field

def test_setup_pk_first_second_key(meta_options: MetaOptions):
    pass

def test_setup_pk_first_no_primary_key(meta_options: MetaOptions):
    class Field:
        primary_key = False
    field = Field
    meta_options.setup_pk(field)
    assert meta_options.primary_key is None