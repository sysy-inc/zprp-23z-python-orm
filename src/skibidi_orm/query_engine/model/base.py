from pydantic import BaseModel, Field
from pydantic._internal._model_construction import ModelMetaclass
from typing import Any
import inspect
from skibidi_orm.query_engine.model.meta_options import MetaOptions
from skibidi_orm.query_engine.field.field import AutoField


def _is_field(value: Any):
    # Only call contribute_to_class() if it's bound.
    return not inspect.isclass(value) and hasattr(value, "contribute_to_class")


class MetaModel(ModelMetaclass):
    """ A metaclass for model """
    def __new__(cls, name: str, bases: tuple[Any], attrs: dict[str, Any]) -> Any:
        super_new: Any = super().__new__ # type: ignore

        # Ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, MetaModel)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        metadata: dict[str, Any] = {}
        new_attrs: dict[str, Any] = {}

        db_table_name = attrs.pop("__db_table__", name.lower())
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
        """ Adds attribute to class """
        obj.contribute_to_class(cls, obj_name)


class Model(BaseModel, metaclass=MetaModel):
    """ A class to create your own database table """
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    def __init__(self, *args: Any, **kwargs: Any):
        opts: MetaOptions = self._meta # type: ignore
        if len(args) > len(opts.local_fields): # type: ignore
            raise IndexError("Number of args exceeds number of fields")

        fields_iter = iter(opts.local_fields)    # type: ignore
        for val, field in zip(args, fields_iter):
            kwargs[field.name] = val
        for field in fields_iter:
            if field.is_relation and field.column in kwargs:
                    kwargs[field.name] = None
                    self.__fields__[field.column] = Field(default=None)
            elif field.name not in kwargs:
                if field.primary_key:
                    continue
                kwargs[field.name] = field.default
        args = ()
        super().__init__(*args, **kwargs)
        # if primary key is AutoField change it to None
        if isinstance(self._meta.primary_key, AutoField):
            self.pk = None


    def _get_pk_val(self):
        return getattr(self, self._meta.primary_key.name)

    def _set_pk_val(self, value: Any):
        name = self._meta.primary_key.name
        setattr(self, name, value)

    pk = property(_get_pk_val, _set_pk_val)

    def __eq__(self, other: MetaModel):
        if not isinstance(other, Model):
            return NotImplemented
        if type(self) != type(other):
            return False
        my_pk = self.pk
        if my_pk is None:
            return self is other
        return my_pk == other.pk

    def __setattr__(self, name: str, value: Any) -> None:
        if name not in self.__fields__:
            self.__fields__[name] = Field(default=None)
        return super().__setattr__(name, value)
