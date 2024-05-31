from skibidi_orm.query_engine.field.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinValueValidator,
    DecimalValidator,
    BaseValidator
)
from typing import TYPE_CHECKING, Any, Union, Optional, List
import datetime
import decimal


if TYPE_CHECKING:
    from skibidi_orm.query_engine.field.relation_objects import RelationObject
    from skibidi_orm.query_engine.model.base import Model


class Error(Exception):
    """
    Custom Error class
    """
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def is_valid_date(date_string: str) -> Optional[datetime.date]:
    """
    Validates if the given string is a valid date in the format 'YYYY-MM-DD'.
    Args:
        date_string (str): The date string to be validated.
    Returns:
        datetime.datetime: A datetime object representing the parsed date.
    Raises:
        ValueError: If the date string is not in the correct format or is an invalid date.
    """
    try:
        date = datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return datetime.datetime.date(date)
    except ValueError:
        raise ValueError("Invalid date format, expected 'YYYY-MM-DD'")


def is_valid_datetime(datetime_string: str) -> Optional[datetime.datetime]:
    """
    Validates if the given string is a valid datetime in the format 'YYYY-MM-DD HH:MM:SS'.
    Args:
        datetime_string (str): The datetime string to be validated.
    Returns:
        datetime.datetime: A datetime object representing the parsed datetime.
    Raises:
        ValueError: If the datetime string is not in the correct format or is an invalid datetime.
    """
    try:
        datetime_obj = datetime.datetime.strptime(datetime_string, '%Y-%m-%d %H:%M:%S')
        return datetime_obj
    except ValueError:
        raise ValueError


def integer_field_range(type: str) -> tuple[int, int]:
    """
    Function for mocking integer range from a database
    """
    return (1, 10)


class Field:
    instances_count: int = 0

    def __init__(self,
                 null: bool = False,
                 name: str = "",
                 db_column: str = "",
                 unique: bool = False,
                 primary_key: bool = False,
                 max_length: Any = None,
                 default: Any = None,
                 field_type: str = "",
                 related: 'Optional[RelationObject]' = None):
        """
        Initializes a new instance of the Field class.

        Args:
            null (bool): Whether the field can be null. Defaults to False.
            name (str): The name of the field in the Python class. Defaults to an empty string.
            db_column (str): The name of the corresponding column in the database. Defaults to an empty string.
            unique (bool): Whether the field must be unique across the table. Defaults to False.
            primary_key (bool): Whether the field is a primary key. Defaults to False.
            max_length (Any): The maximum length of the field's value. Defaults to None.
            default (Any): The default value for the field. Defaults to None.
            field_type (str): The type of the field. Defaults to an empty string.
            related (Union[RelationObject, None]): The related field for foreign key relationships. Defaults to None.

        Attributes:
            null (bool): Whether the field can be null.
            name (str): The name of the field in the Python class.
            db_column (str): The name of the corresponding column in the database.
            unique (bool): Whether the field must be unique across the table.
            primary_key (bool): Whether the field is a primary key.
            max_length (Any): The maximum length of the field's value.
            default (Any): The default value for the field.
            validators (List[object]): A list of validators to validate the field's value.
            field_type (str): The type of the field.
            remote_field (Union[RelationObject, None]): The related field for foreign key relationships.
            is_relation (bool): Whether the field is a foreign key relationship.
            instances_count (int): The number of Field instances created.
        """
        self.null = null,
        self.name = name                # python's field name
        self.db_column = db_column      # column name in db
        self.unique = unique
        self.primary_key = primary_key
        self.max_length = max_length
        self.default = default
        self.validators: List[Union[BaseValidator, DecimalValidator]] = []    # list of validators to validate a value
        self.field_type = field_type
        self.remote_field = related
        self.is_relation = self.remote_field is not None

        self.instances_count = Field.instances_count
        Field.instances_count += 1

    def __str__(self):
        """
        Returns pythonic name of the field
        """
        return self.name

    def get_type(self) -> str:
        """
        Gets the type of the field.

        Returns:
            str: The type of the field as a string.
        """
        return ""

    def __lt__(self, other: Any) -> bool:
        return self.instances_count < other.instances_count

    def __eq__(self, other: Any) -> bool:
        return self.instances_count == other.instances_count

    def set_attr_names(self, name: str):
        """
        Sets the attribute names for the object.

        If `self.name` is not already set, it assigns the provided `name` to `self.name`.
        Similarly, if `self.db_column` is not already set, it assigns `self.name` to `self.column`.

        Args:
            name (str): The name to be set if `self.name` is not already defined.

        """
        self.name = self.name or name
        self.column = self.db_column or self.name

    def contribute_to_class(self, cls: Model, name: str):
        """
        Contributes this field to the given class.

        This method sets the attribute names, assigns the model class to the field,
        and adds the field to the class's metadata. If the field has a column name,
        it sets an attribute on the class with the field's name.

        Args:
            cls (Model): The class to which this field is being added.
            name (str): The name of the field.

        """ 
        self.set_attr_names(name)
        self.model = cls
        cls._meta.add_field(self)
        if self.column:
            setattr(cls, self.name, 1)

    def to_python(self, value: Any):
        """
        Converts input to the expected python data type.
        Args:
            value: the input value to be converted
        """
        return value

    def db_type(self, conn: dict[str, str]) -> object:
        """
        Returns the database column type for this field for a given connection from a converter dictionary.

        Args:
            conn (dict[str, str]): A dictionary representing the connection, where the keys are the types and the values are the corresponding database column types.

        Returns:
            object: The database column type for this field. Returns None if the type is not found in the connection dictionary.

        """
        try:
            column_type = conn[self.get_type()]
        except KeyError:
            return None
        return column_type

    def check(self):
        """
        Calls all validators that need to be checked for a field type.
        """
        pass


class IntegerField(Field):
    def __init__(self, *args: Any, **kwargs: Any):
        """
        Initializes a new instance of the class.

        Attributes:
            validators (List[DecimalValidator]): A list of validators for the field.
        """
        super().__init__(*args, **kwargs)
        self.add_validators()

    def get_type(self) -> str:
        return "IntegerField"

    def to_python(self, value: Any) -> Optional[int]:
        if value is None:
            return value
        else:
            try:
                return int(value)
            except (ValueError, TypeError):
                raise Error("Value must be an integer")

    def add_validators(self):
        min_value, max_value = integer_field_range(self.get_type())
        self.validators.append(MaxValueValidator(max_value))        
        self.validators.append(MinValueValidator(min_value))


class BigIntegerField(IntegerField):
    def get_type(self) -> str:
        return "BigIntegerField"


class SmallIntegerField(IntegerField):
    def get_type(self) -> str:
        return "SmallIntegerField"


class PositiveIntegerField(IntegerField):
    def get_type(self) -> str:
        return "PositiveIntegerField"


class PositiveBigIntegerField(BigIntegerField):
    def get_type(self) -> str:
        return "PositiveBigIntegerField"


class PositiveSmallIntegerField(SmallIntegerField):
    def get_type(self) -> str:
        return "PositiveSmallIntegerField"


class DecimalField(Field):
    def __init__(self, max_digits: int, decimal_places: int, **kwargs: Any):
        """
        Initializes a new instance of the class.

        Args:
            max_digits (int): The maximum number of digits allowed.
            decimal_places (int): The number of decimal places allowed.
            **kwargs: Additional keyword arguments.

        Attributes:
            max_digits (int): The maximum number of digits allowed.
            decimal_places (int): The number of decimal places allowed.
            validators (List[DecimalValidator]): A list of validators for the field.
        """
        super().__init__(**kwargs)                                                    
        self.decimal_places = decimal_places
        self.max_digits = max_digits
        self.validators.append(DecimalValidator(self.max_digits, self.decimal_places))
    
    def get_name(self) -> str:
        return "DecimalField"

    def check(self, **kwargs: Any):
        super().check(**kwargs)
        self._check_max_digits()
        self._check_decimal_places()
        self._check_max_digits_and_decimal_places()

    def _check_max_digits(self):
        """
        Checks if the max_digits attribute is valid.

        Raises:
            Error: If the max_digits attribute is not a positive integer.
        """
        msg = ""
        try:
            max_digits = int(self.max_digits)
            if max_digits <= 0:
                msg = "max_digits must be an integer greater than 0."
                raise ValueError()
        except (ValueError, TypeError):
            if len(msg) == 0:
                msg = "DecimalField must define max_digits attribute"
            raise Error(msg)

    def _check_decimal_places(self):
        """
        Checks if the decimal_places attribute is valid.

        Raises:
            Error: If the decimal_places attribute is not a non-negative integer.
        """
        msg = ""
        try:
            decimal_places = int(self.decimal_places)
            if decimal_places < 0:
                msg = "decimal_places must be an integer greater or equal to 0."
                raise ValueError()
        except (TypeError, ValueError):
            if len(msg) == 0:
                msg = "DecimalField must define decimal_places attribute"
            raise Error(msg)

    def _check_max_digits_and_decimal_places(self):
        """
        Checks if the combination of max_digits and decimal_places is valid.

        Raises:
            Error: If decimal_places is greater than max_digits.
        """
        if int(self.decimal_places) > int(self.max_digits):
            raise Error("decimal_places must be greater or equal to max_digits.")
    
    def to_python(self, value: Any) -> Optional[decimal.Decimal]:
        if value is None:
            return value
        try:
            decimal_value = decimal.Decimal(value)
        except (decimal.InvalidOperation, TypeError, ValueError):
            raise Error("Value must be a decimal.")
        if not decimal_value.is_finite():
            raise Error("Value must be a decimal.")
        return decimal_value


class FloatField(Field):
    def get_name(self) -> str:
        return "FloatField"
    
    def to_python(self, value: Any) -> Optional[float]:
        if value is None:
            return value
        else:
            try:
                return float(value)
            except (ValueError, TypeError):
                raise Error("Value must be a float")


class CharField(Field):
    def __init__(self, *args: Any, **kwargs: Any):   
        super().__init__(*args, **kwargs)   
        if self.max_length is not None:     
            self.validators.append(MaxLengthValidator(self.max_length))

    def get_name(self) -> str:
        return "CharField"

    def to_python(self, value: Any) -> Optional[str]:
        if isinstance(value, str) or value is None:
            return value
        return str(value)
    
    def check(self, **kwargs: Any):
        super().check(**kwargs)
        self._check_max_length()
    
    def _check_max_length(self):
        """
        Checks if the max_length attribute is valid.

        Raises:
            Error: If max_length is not None and is not a positive integer.
        """
        if self.max_length is not None:
            if not isinstance(self.max_length, int) or self.max_length < 1:
                raise Error("max_length must be an integer greater than 0")


class TextField(Field):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def get_name(self) -> str:
        return "TextField"

    def to_python(self, value: Any) -> Optional[str]:
        if value is None:
            return value
        return str(value)


class BooleanField(Field):
    def get_name(self):
        return "BooleanField"
    
    def to_python(self, value: Any) -> Optional[bool]:
        if self.null and value in (None, "", [], {}):
            return None
        elif value in (True, False):
            return bool(value)
        elif value in ('1', 't', 'True'):
            return True
        elif value in ('0', 'f', 'False'):
            return False
        elif self.null:
            raise Error("Invalid value (must be either True, False or None)")
        else:
            raise Error("Invalid value (must be either True or False)")


class DateField(Field):
    def get_name(self) -> str:
        return "DateField"
    
    def to_python(self, value: Union[str, datetime.date, datetime.datetime]) -> Optional[datetime.date]:
        if isinstance(value, datetime.datetime):
            return value.date()
        if isinstance(value, datetime.date):
            return value
        try:
            parsed = is_valid_date(value)
            if parsed is not None:
                return parsed
        except ValueError:
            raise Error("Given date is invalid.")


class DateTimeField(DateField):

    def get_name(self) -> str:
        return "DateTimeField"
    
    def to_python(self, value: Union[str, datetime.date, datetime.datetime]) -> Optional[datetime.datetime]:
        if isinstance(value, datetime.datetime):
            return value
        elif isinstance(value, datetime.date):
            value = datetime.datetime(value.year, value.month, value.day)
            return value

        elif len(value) == 10:
            try:
                parsed = is_valid_date(value)
                if parsed is not None:
                    return datetime.datetime(parsed.year, parsed.month, parsed.day)
            except ValueError:
                raise Error("Given date is invalid.")
        else:
            try:
                parsed = is_valid_datetime(value)
                if parsed is not None:
                    return parsed
            except ValueError:
                raise Error("Given datetime is invalid.")


class AutoField(Field):
    pass


