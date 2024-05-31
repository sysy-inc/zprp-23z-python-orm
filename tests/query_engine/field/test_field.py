import pytest
import math
import decimal
from datetime import datetime, date
from skibidi_orm.query_engine.field.field import (
    BooleanField,
    IntegerField,
    FloatField,
    DecimalField,
    CharField,
    DateField,
    DateTimeField,
    Error,
)


def test_instances_count():
    field1 = IntegerField()
    field2 = BooleanField()
    field3 = FloatField()
    assert field1.instances_count == 0
    assert field2.instances_count == 1
    assert field3.instances_count == 2


def test_comparison():
    field1 = IntegerField()
    field2 = BooleanField()
    assert field1 < field2


def test_equal():
    field1 = IntegerField()
    field2 = BooleanField()
    assert field1 != field2


# IntegerField to_python

def test_IntegerField_int_str():
    field = IntegerField()
    assert 5 == field.to_python('5')


def test_IntegerField_bool():
    field = IntegerField()
    assert 1 == field.to_python(True)


def test_IntegerField_none():
    field = IntegerField()
    assert field.to_python(None) is None


def test_IntegerField_char_str():
    field = IntegerField()
    with pytest.raises(Error):
        field.to_python('1o7')


def test_IntegerField_float():
    field = IntegerField()
    assert 1 == field.to_python(1.54)


# IntegerField validators

def test_IntegerField_validators():
    field = IntegerField()
    has_limit_10 = any(obj.limit == 10 for obj in field.validators)     # type: ignore
    assert has_limit_10 is True


def test_IntegerField_MinValidator():
    field = IntegerField()
    has_limit_1 = any(obj.limit == 1 for obj in field.validators)       # type: ignore
    assert has_limit_1 is True


# DecimalField to_python

def test_DecimalField_float_str():
    field = DecimalField(10, 5)
    assert decimal.Decimal('5.1452') == field.to_python('5.1452')


def test_DecimalField_bool():
    field = DecimalField(10, 5)
    assert 1 == field.to_python(True)


def test_DecimalField_none():
    field = DecimalField(10, 5)
    assert field.to_python(None) is None


def test_IDecimalField_char_str():
    field = DecimalField(10, 5)
    with pytest.raises(Error):
        field.to_python('1o7')


def test_DecimalField_float():
    field = DecimalField(10, 5)
    assert 1.54 == field.to_python(1.54)


def test_DecimalField_inf():
    field = DecimalField(10, 5)
    with pytest.raises(Error):
        field.to_python(math.inf)


# DecimalField check
# max_digits

def test_DecimalField_max_digits_float():
    field = DecimalField(10.5412, 5)          # type: ignore
    field.check()


def test_DecimalField_max_digits_str():
    field = DecimalField('ol4', 5)          # type: ignore
    with pytest.raises(Error):
        field.check()


def test_DecimalField_max_digits_less_than_0():
    field = DecimalField(-3, 5)          # type: ignore
    with pytest.raises(Error):
        field.check()


# decimal_places

def test_DecimalField_decimal_places_float():
    field = DecimalField(10, 5.5412)          # type: ignore
    field.check()


def test_DecimalField_decimal_places_str():
    field = DecimalField(10, 'ol4')          # type: ignore
    with pytest.raises(Error):
        field.check()


def test_DecimalField_decimal_places_less_than_0():
    field = DecimalField(9, -5)          # type: ignore
    with pytest.raises(Error):
        field.check()


# max_digits_and_decimal_places

def test_DecimalField_decimal_places_less_than_max_digits():
    field = DecimalField(2, 4)          # type: ignore
    with pytest.raises(Error):
        field.check()


# DecimalField validators
def test_DecimalField_validators():
    field = DecimalField(7, 13)
    has_validator = any(
            hasattr(obj, 'max_digits') and hasattr(obj, 'decimal_places') and 
            obj.max_digits == 7 and obj.decimal_places == 13 for obj in field.validators)       # type: ignore
    assert has_validator is True


# FloatField to_python 
def test_FloatField_int_str():
    field = FloatField()
    assert 5.14 == field.to_python('5.14')


def test_FloatField_bool():
    field = FloatField()
    assert 1 == field.to_python(True)


def test_FloatField_none():
    field = FloatField()
    assert field.to_python(None) is None


def test_FloatField_char_str():
    field = FloatField()
    with pytest.raises(Error):
        field.to_python('1o7')


def test_FloatField_float():
    field = FloatField()
    assert 1.54 == field.to_python(1.54)


# CharField to_python 

def test_CharField_int_str():
    field = CharField()
    assert '5.14' == field.to_python('5.14')


def test_CharField_bool():
    field = CharField()
    assert 'True' == field.to_python(True)


def test_CharField_none():
    field = CharField()
    assert field.to_python(None) is None


def test_CharField_float():
    field = CharField()
    assert '1.54' == field.to_python(1.54)


# CharField max_length

def test_CharField_max_length_float():
    field = CharField(max_length=1.5)
    with pytest.raises(Error):
        field.check()


def test_CharField_max_length_str():
    field = CharField(max_length='1.5')
    with pytest.raises(Error):
        field.check()


def test_CharField_max_length_less_than_1():
    field = CharField(max_length=0)
    with pytest.raises(Error):
        field.check()


# TextField methods are the exact same as CharField methods

# BooleanField to_python

def test_BooleanField_int_str():
    field = BooleanField()
    with pytest.raises(Error):
        field.to_python('5.14')


def test_BooleanField_bool():
    field = BooleanField()
    assert field.to_python(True) is True


def test_BooleanField_none():
    field = BooleanField()
    assert field.to_python(None) is None


def test_BooleanField_char_number():
    field = BooleanField()
    with pytest.raises(Error):
        field.to_python(45)


def test_BooleanField_char():
    field = BooleanField()
    assert field.to_python('f') is False


# DateField to_python

def test_DateField_date():
    date1 = date(2002, 10, 28)
    field = DateField()
    date2 = field.to_python(date1)
    assert date2 == date1


def test_DateField_datetime():
    date1 = datetime(2002, 10, 28, 12, 54, 00)
    field = DateField()
    date2 = field.to_python(date1)
    assert date2 == date(2002, 10, 28)


def test_DateField_str_valid():
    date1 = '2002-10-28'
    field = DateField()
    date2 = field.to_python(date1)
    assert date2 == date(2002, 10, 28)


def test_DateField_str_invalid():
    date1 = '2002-10-k8'
    field = DateField()
    with pytest.raises(Error):
        field.to_python(date1)

# DatetimeField to_python


def test_DatetimeField_date():
    date1 = date(2002, 10, 28)
    field = DateTimeField()
    date2 = field.to_python(date1)
    assert date2 == datetime(2002, 10, 28, 00, 00)


def test_DatetimeField_datetime():
    date1 = datetime(2002, 10, 28, 10, 14, 6)
    field = DateTimeField()
    date2 = field.to_python(date1)
    assert date2 == date1


def test_DatetimeField_strDate_valid():
    date1 = '2002-10-28'
    field = DateTimeField()
    date2 = field.to_python(date1)
    assert date2 == datetime(2002, 10, 28, 00, 00)


def test_DatetimeField_strDate_invalid():
    date1 = '2002-10-k8'
    field = DateTimeField()
    with pytest.raises(Error):
        field.to_python(date1)


def test_DatetimeField_strDatetime_valid():
    date1 = '2002-10-28 13:15:22'
    field = DateTimeField()
    date2 = field.to_python(date1)
    assert date2 == datetime(2002, 10, 28, 13, 15, 22)


def test_DatetimeField_strDatetime_invalid():
    date1 = '2002-10-k8-00-45'
    field = DateTimeField()
    with pytest.raises(Error):
        field.to_python(date1)