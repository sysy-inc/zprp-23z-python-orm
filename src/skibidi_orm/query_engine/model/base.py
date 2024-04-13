""" A model class for mapping database table """

from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from typing import Any, Tuple, Dict, List
import inspect
import bisect

def convert_name_to_table(name: str) -> str:
    return name

def check_db_name_is_correct(db_table_name: str) -> bool:
    return True

def _is_field(value: Any):
    # Only call contribute_to_class() if it's bound.
    return not inspect.isclass(value) and hasattr(value, "contribute_to_class")

class MetaOptions:
    """ A subsidiary to storage additional information"""
    def __init__(self, meta: Dict[str, Any]):
        self.fields = []
        self.db_table = meta['db_table']
        self.primary_key = None
        self.local_field: List[Any] = []

    def contribute_to_class(self, cls: Any, obj_name: str):
        """ Adds atrributes to classes """
        cls._meta = self
        self.model = cls

    def add_field(self, field: Any):
        """ Adds database column """
        bisect.insort(self.local_fields, field) # type: ignore
        self.setup_pk(field)

    def setup_pk(self, field: Any):
        """ Setup the primary key """
        if self.pk and field.primary_key:
            # TODO raise error
            pass
        elif not self.pk and field.primary_key:
            self.pk = field

    def _prepare(self, model: Any):
        # TODO check if attrs' names are correct
        # TODO check if is primary key
        # TODO check if atrr db_column is unique
        pass


class MetaModel(ModelMetaclass):
    """ A metaclass for model """
    def __new__(cls, name: str, bases: Tuple[Any], attrs: Dict[str, Any]) -> Any:
        super_new: Any = super().__new__ # type: ignore

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [ b for b in bases if isinstance(b, MetaModel) ]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # TODO add database config

        metadata: Dict[str, Any] = {}
        new_attrs: Dict[str, Any] = {}

        # TODO improve convert db table name and check if name is correct
        db_table_name = attrs.pop("db_table", None)
        if db_table_name:
            check_db_name_is_correct(db_table_name)
        else:
            db_table_name = convert_name_to_table(name)
        metadata["db_table"] = db_table_name

        field_attrs = {}
        for obj_name, obj in attrs.items():
            if _is_field(obj):
                field_attrs[obj_name] = obj
            else:
                new_attrs[obj_name] = obj
        new_class = super_new(cls, name, bases, new_attrs)
        new_class.add_to_class("_meta", MetaOptions(metadata))

        for obj_name, obj in field_attrs.items(): # type: ignore
            new_class.add_to_class(obj_name, obj)

        new_class._meta._prepare(new_class)
        return new_class

    def add_to_class(cls, obj_name: str, obj: Any): # type: ignore
        """ Adds atrribute to class """
        obj.contribute_to_class(cls, obj_name)





class Model(BaseModel):
    """ A class to create your own database table """
    # TODO add information about inheritance
    pass