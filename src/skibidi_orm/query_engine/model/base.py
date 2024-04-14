""" A model class for mapping database table """

from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from typing import Any
import inspect
from skibidi_orm.query_engine.model.meta_options import MetaOptions

def convert_name_to_table(name: str) -> str:
    return name

def check_db_name_is_correct(db_table_name: str) -> bool:
    return True

def _is_field(value: Any):
    # Only call contribute_to_class() if it's bound.
    return not inspect.isclass(value) and hasattr(value, "contribute_to_class")


class MetaModel(ModelMetaclass):
    """ A metaclass for model """
    def __new__(cls, name: str, bases: tuple[Any], attrs: dict[str, Any]) -> Any:
        super_new: Any = super().__new__ # type: ignore

        # TODO subclass is final

        # Also ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [ b for b in bases if isinstance(b, MetaModel) ]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # TODO add database config

        metadata: dict[str, Any] = {}
        new_attrs: dict[str, Any] = {}

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
    def __init__(self, *args: Any, **kwargs: Any):
        opts: MetaOptions = self._meta # type: ignore
        if len(args) > len(opts.local_field): # type: ignore
            # Daft, but matches old exception sans the err msg.
            raise IndexError("Number of args exceeds number of fields")

        fields_iter = iter(opts.local_fields)    # type: ignore
        for val, field in zip(args, fields_iter):
            setattr(self, field.attname, val)
        for field in fields_iter:
            val = kwargs.pop(field.name, None)
            if not val:
                val = field.get_default()       # TODO add error
            setattr(self, field.attname, val)
