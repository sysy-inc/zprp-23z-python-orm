from typing import Any
import decimal


class ValidationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class BaseValidator:
    def __init__(self, limit: int):
        self.limit = limit
        self.msg = f"Value is not meeting the criteria (should be equal to {self.limit})"

    def __call__(self, value: Any):
        if not self.compare(value, self.limit):
            raise ValidationError(self.msg)

    def compare(self, a: Any, b: Any) -> bool:
        return a == b


class MaxLengthValidator(BaseValidator):
    def __init__(self, limit: int):
        super().__init__(limit)
        self.msg = f"Value is not meeting the criteria (length should be less than {self.limit})"

    def compare(self, a: Any, b: Any) -> bool:
        a = len(a)
        return a <= b


class MinLengthValidator(BaseValidator):
    def __init__(self, limit: int):
        super().__init__(limit)
        self.msg = f"Value is not meeting the criteria (length should be more than {self.limit})"

    def compare(self, a: Any, b: Any) -> bool:
        a = len(a)
        return a >= b


class MaxValueValidator(BaseValidator):
    def __init__(self, limit: int):
        super().__init__(limit)
        self.msg = f"Value is not meeting the criteria (should be less than {self.limit})"

    def compare(self, a: Any, b: Any) -> bool:
        return a < b


class MinValueValidator(BaseValidator):
    def __init__(self, limit: int):
        super().__init__(limit)
        self.msg = f"Value is not meeting the criteria (should be more than {self.limit})"

    def compare(self, a: Any, b: Any) -> bool:
        return a > b


class DecimalValidator:
    def __init__(self, max_digits: int, decimal_places: int):
        self.decimal_places = decimal_places
        self.max_digits = max_digits

    def __call__(self, value: decimal.Decimal):
        digit_tuple, exponent = value.as_tuple()[1:]
        if exponent in {"F", "n", "N"}:
            raise ValidationError("Value must be a decimal.")
        if isinstance(exponent, int) and exponent >= 0:                                       
            digits = len(digit_tuple)
            if digit_tuple != (0,):
                digits += exponent                               
            decimals = 0
        else:
            if isinstance(exponent, int) and abs(exponent) > len(digit_tuple):
                digits = decimals = abs(exponent)
            elif isinstance(exponent, int):
                digits = len(digit_tuple)
                decimals = abs(exponent)
            else:
                decimals = 0
                digits = 0
        whole_digits = digits - decimals

        if self.max_digits and digits > self.max_digits:
            raise ValidationError("Number of digits is excedeed.")
        if self.decimal_places and decimals > self.decimal_places:
            raise ValidationError("Number of decimals is excedeed.")
        if whole_digits > (self.max_digits - self.decimal_places):
            raise ValidationError("Number of digits before decimal is excedeed")
