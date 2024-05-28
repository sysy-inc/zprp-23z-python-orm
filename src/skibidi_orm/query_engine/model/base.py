from pydantic import BaseModel, Field
from pydantic._internal._model_construction import ModelMetaclass
from typing import Any
import inspect
from skibidi_orm.query_engine.model.meta_options import MetaOptions
from skibidi_orm.query_engine.field.field import AutoField
from skibidi_orm.query_engine.connection.session import Session


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
            if field.is_relation and field.db_column in kwargs:
                kwargs[field.name] = None   # add none to have attr value
            elif field.name not in kwargs:
                kwargs[field.name] = field.default
        args = ()
        super().__init__(*args, **kwargs)

        # if primary key is AutoField change it to None
        if isinstance(self._meta.primary_key, AutoField):
            self.pk = None

        # if foreign key is given by id set it correct
        for field in self._meta.relation_fields:
            value = kwargs.get(field.db_column, None)
            object.__setattr__(self, field.db_column, value)
        self._changes: dict [str, str] = {}


    def _get_pk_val(self):
        return getattr(self, self._meta.primary_key.name)

    def _set_pk_val(self, value: Any):
        name = self._meta.primary_key.name
        setattr(self, name, value)

    pk = property(_get_pk_val, _set_pk_val)

    def __eq__(self, other: object):
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
        super().__setattr__(name, value)
        if hasattr(self, '_changes') and name != '_changes':
            self._changes[name] = value
            if hasattr(self, '_session'):
                self._session.changed(self)
        if name in self._meta.relation_fields_name():
            field = self._meta.get_relation_field(name)
            obj_id = value.pk if value else None
            if obj_id != object.__getattribute__(self, field.db_column):
                object.__setattr__(self, field.db_column, None)
        elif name in self._meta.relation_fields_column():
            field = self._meta.get_relation_field(name)
            obj_id = object.__getattribute__(self, field.name).pk if object.__getattribute__(self, field.name) else None
            if obj_id != value:
                object.__setattr__(self, field.name, None)

    def __getattribute__(self, name: str) -> Any:
        value = super().__getattribute__(name)
        if value is None and name in self._meta.relation_fields_name():
            field = self._meta.get_relation_field(name)
            if object.__getattribute__(self, field.db_column):
                # if id select obj from db
                # TODO add select if is id
                value = 5
            # return none if not id
        elif value is None and name in self._meta.relation_fields_column():
            field = self._meta.get_relation_field(name)
            if object.__getattribute__(self, field.name):
                value = object.__getattribute__(self, field.name).pk
        return value

    def _get_name_and_pk(self):
        return (self._meta.db_table, self.pk)

    def _get_attr_values(self):
        atrr_values : list[Any] = []
        for field in self._meta.local_fields:
            if field.is_relation:
                atrr_values.append((field.db_column, getattr(self, field.db_column)))
            else:
                value = getattr(self, field.name)
                if value is not None:
                    atrr_values.append((field.name, value))
        return atrr_values

    def _update_changes_db(self):
        changes = self._changes
        self._changes = {}
        return changes

    def _add_session(self, session: Session):
        self._session = session

    def _remove_session(self):
        self._session = None

    def _is_pk_none(self):
        return self.pk is None and isinstance(self._meta.primary_key, AutoField)

    def _get_db_pk(self):
        return self._meta.primary_key.db_column, self.pk