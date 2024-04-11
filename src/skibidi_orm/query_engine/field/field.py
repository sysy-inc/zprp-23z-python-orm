from dataclasses import dataclass, field
from typing import Any

@dataclass
class Field:
    null: bool = field(default=False, repr=False)
    name: str = field(default="")            # python's field name
    db_column: str = field(default="")        # column name in db
    unique: bool = field(default=False, repr=False)
    primary_key: bool = field(default=False, repr=False)
    max_length: int = field(default=100, repr=False, metadata={"min_value": 0})
    default = None                              #TODO do sth about it
    validators: list[function] = field(default_factory=list, repr=False)  # list of validators to validate a type
    field_type: str = field(default="")

    def __str__(self):
        """
        Returns pythonic name of the field
        """
        #TODO return also field model's name
        return self.name
    
    def deconstruct(self):
        """
        Returns essential data for the field to be recreated from file
        ie name, list of positional args, list of keyword args, import path of the field
        """
        pass

    def to_python(self, value: Any):
        """
        Converts input to the expected python data type.
        To be overriden in subclasses.
        """
        return value
    
    def db_type(self, conn_type: str):
        """
        Returns database column type for this field for given connection from CONVERTER DICTIONARY
        """
        pass

    def to_db_type(self, value:Any, conn_type: str):
        """
        Prepares the value to be saved into database
        """
        pass
        #TODO implement functionality

    def validate(self, **kwargs):
        """
        Returns list of basic validators that need to be checked for every field type. 
        Specific validators nedd to be added in overriden methods
        ie checking if field name does not have any illegal chars
        """
        pass

    #TODO implement validators & errors 