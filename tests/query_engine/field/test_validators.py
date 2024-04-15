import pytest
import decimal
from skibidi_orm.query_engine.field.validators import (
    BaseValidator,
    MaxLengthValidator,
    MinLengthValidator,
    MaxValueValidator,
    MinValueValidator,
    DecimalValidator,
    ValidationError
)


# Base Validator

def test_BaseValidator_equal():
    base_valid = BaseValidator(5)
    base_valid(5)


def test_BaseValidator_not_equal():
    base_valid = BaseValidator(5)
    with pytest.raises(ValidationError):
        base_valid(6)


# Max Length Validator

def test_MaxLengthValidator_less():
    max_len_valid = MaxLengthValidator(5)
    max_len_valid(4)


def test_MaxLengthValidator_more():
    max_len_valid = MaxLengthValidator(5)
    with pytest.raises(ValidationError):
        max_len_valid(6)


# Min Length Validator

def test_MinLengthValidator_more():
    min_len_valid = MinLengthValidator(5)
    min_len_valid(6)


def test_MinLengthValidator_less():
    min_len_valid = MinLengthValidator(5)
    with pytest.raises(ValidationError):
        min_len_valid(4)


# Max Value Validator

def test_MaxValueValidator_less():
    max_val_valid = MaxValueValidator(5)
    max_val_valid(4)


def test_MaxValueValidator_more():
    max_val_valid = MaxValueValidator(5)
    with pytest.raises(ValidationError):
        max_val_valid(6)


# Min Value Validator

def test_MinValueValidator_more():
    min_val_valid = MinValueValidator(5)
    min_val_valid(6)


def test_MinValueValidator_less():
    min_val_valid = MinValueValidator(5)
    with pytest.raises(ValidationError):
        min_val_valid(4)


# Decimal Validator

def test_DecimalValidator_decimals_exceeded():
    decimal_valid = DecimalValidator(10, 5)
    with pytest.raises(ValidationError):
        decimal_valid(decimal.Decimal('6.456123'))


def test_DecimalValidator_digits_exceeded():
    decimal_valid = DecimalValidator(10, 5)
    with pytest.raises(ValidationError):
        decimal_valid(decimal.Decimal('44412369874.4567'))


def test_DecimalValidator_digits_upper_limit():
    decimal_valid = DecimalValidator(10, 5)
    decimal_valid(decimal.Decimal('45612.45674'))


def test_DecimalValidator_str():
    decimal_valid = DecimalValidator(10, 5)
    with pytest.raises(AttributeError):
        decimal_valid('abc')            # type: ignore


def test_DecimalValidator_exponent_below_zero():
    decimal_valid = DecimalValidator(10, 5)
    decimal_valid(decimal.Decimal('0.008'))
