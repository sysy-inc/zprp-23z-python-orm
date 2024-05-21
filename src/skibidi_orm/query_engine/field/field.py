from skibidi_orm.query_engine.field.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinValueValidator,
    DecimalValidator
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skibidi_orm.query_engine.field.relation_objects import RelationObject
from typing import Any, List, Type, Union
import decimal


class NOT_PROVIDED:
    """
    Notes that no value has been passed to the 'default' attr in Field class
    as 'None' could be considered as a default value
    """
    pass


class Error(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Field:
    instances_count: int = 0

    def __init__(self, 
                 null: bool = False,
                 name: str = "", 
                 db_column: str = "",
                 unique: bool = False,
                 primary_key: bool = False,
                 max_length: Union[int, None] = None,       
                 default: Any = NOT_PROVIDED,
                 validators: List[object] = [],
                 field_type: str = "",
                 related: 'Union[RelationObject, None]' = None):
        self.null = null,
        self.name = name                # python's field name
        self.db_column = db_column      # column name in db
        self.unique = unique
        self.primary_key = primary_key
        self.max_length = max_length
        self.default = default                        
        self.validators = validators    # list of validators to validate a value; this collects all validators from all subclasses instances
        self.field_type = field_type
        self.remote_field = related
        self.is_relation = self.remote_field is not None

        self.instances_count = Field.instances_count
        Field.instances_count += 1
    
    def __str__(self):
        """
        Returns pythonic name of the field
        """
        # if hasattr(self, "model"):
        #    return str(self.model), self.name
        return self.name

    def get_type(self) -> str:
        return ""
    
    def __lt__(self, other: Any) -> bool:
        return self.instances_count < other.instances_count
    
    def __eq__(self, other: Any) -> bool:
        return self.instances_count == other.instances_count
    
    def set_attr_names(self, name: str):
        self.name = self.name or name
        self.column = self.db_column or self.name
    
    def contribute_to_class(self, cls: Type[BaseException], name: str):     # change class here!!
        self.set_attr_names(name)
        self.model = cls
        cls._meta.add_field(self)           # type: ignore
        if self.column:
            setattr(cls, self.name, 1)

    def to_python(self, value: Any):
        """
        Converts input to the expected python data type.
        To be overriden in subclasses.
        """
        return value
    
    def db_type(self, conn: dict[str, str]) -> object:
        """
        Returns database column type for this field for given connection from CONVERTER DICTIONARY
        """
        try:
            column_type = conn[self.get_type()]
        except KeyError:
            return None
        return column_type

    def check(self, **kwargs: Any):      
        """
        Calls basic validators that need to be checked for every field type. 
        Specific validators nedd to be added in overriden methods
        """
        pass


class IntegerField(Field):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.add_validators()
        
    def get_type(self) -> str:
        return "IntegerField"
    
    def to_python(self, value: Any):
        if value is None:
            return value
        else:
            try:
                return int(value)
            except (ValueError, TypeError):
                raise Error("Value must be an integer")
    
    def add_validators(self):
        # TODO optimize it
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
        if int(self.decimal_places) > int(self.max_digits):
            raise Error("decimal_places must be greater or equal to max_digits.")
    
    def to_python(self, value: Any):
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
    
    def to_python(self, value: Any):
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

    def to_python(self, value: Any) -> object:
        if isinstance(value, str) or value is None:
            return value
        return str(value)
    
    def check(self, **kwargs: Any):
        super().check(**kwargs)
        self._check_max_length()
    
    def _check_max_length(self):
        if self.max_length is not None:
            if not isinstance(self.max_length, int) or self.max_length < 1:     # type: ignore
                raise Error("max_length must be an integer greater than 0")


class TextField(Field):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def get_name(self) -> str:
        return "TextField"

    def to_python(self, value: Any):
        if isinstance(value, str) or value is None:
            return value
        return str(value)


class BooleanField(Field):
    def get_name(self):
        return "BooleanField"
    
    def to_python(self, value: Any):
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
    def get_name(self):
        return "DateField"
    # TODO add logic


class DateTimeField(Field):
    def get_name(self):
        return "DateTimeField"
    # TODO add logic


class AutoField():
    pass
    # TODO add logic


def integer_field_range(type: str) -> tuple[int, int]:
    """
    Function for mocking integer range from a database
    """
    return (1, 10)
