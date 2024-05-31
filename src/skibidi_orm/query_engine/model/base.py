"""
Module handles managing database model instances with attributes and relationships.
"""

from pydantic import BaseModel, Field
from pydantic._internal._model_construction import ModelMetaclass
from typing import Any, TYPE_CHECKING
import inspect
from skibidi_orm.query_engine.model.meta_options import MetaOptions
from skibidi_orm.query_engine.field.field import AutoField

if TYPE_CHECKING:
    from skibidi_orm.query_engine.connection.session import Session


def _is_field(value: Any):
    """Check if a value is a field in a model.

    This function determines if a given value is a field in model by
    checking if it has the `contribute_to_class` attribute and is not a class.

    Args:
        value (Any): The value to be checked.

    Returns:
        bool: True if the value is a field, False otherwise.
    """
    return not inspect.isclass(value) and hasattr(value, "contribute_to_class")


class MetaModel(ModelMetaclass):
    """A metaclass for model.

    This metaclass is responsible for setting up the metadata and attributes
    for models. It handles the initialization of fields, table
    names, and other metadata.
    """

    def __new__(cls, name: str, bases: tuple[Any], attrs: dict[str, Any]) -> Any:
        """Create a new instance of the model class.

        This method sets up the metadata and fields for the model class. It ensures
        that the initialization is only performed for subclasses of Model, excluding
        the Model class itself.

        Args:
            cls (type): The metaclass.
            name (str): The name of the new class.
            bases (tuple[Any]): The base classes of the new class.
            attrs (dict[str, Any]): The attributes of the new class.

        Returns:
            Any: The new class.
        """
        super_new: Any = super().__new__ # type: ignore

        field_attrs = {}

        # Ensure initialization is only performed for subclasses of Model
        # (excluding Model class itself).
        parents = [b for b in bases if isinstance(b, MetaModel)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        # add parents' local field
        else:
            for parent in parents:
                if hasattr(parent, '_meta'):
                    meta = getattr(parent, '_meta')
                    for field in meta.local_fields:
                        field_attrs[field.name] = field

        metadata: dict[str, Any] = {}
        new_attrs: dict[str, Any] = {}

        db_table_name = attrs.pop("__db_table__", name.lower())
        metadata["db_table"] = db_table_name

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

    def add_to_class(cls, obj_name: str, obj: Any):
        """Add an attribute to the class.

        This method adds a specified attribute to the class.

        Args:
            cls (type): The class to add the attribute to.
            obj_name (str): The name of the attribute.
            obj (Any): The attribute to add.
        """
        obj.contribute_to_class(cls, obj_name)


class Model(BaseModel, metaclass=MetaModel):
    """A class to create your own database table.

    This class represents a database model, handling initialization of fields,
    setting primary keys, and managing relationships and attributes.

    """
    class Config:
        arbitrary_types_allowed = True
        allow_population_by_field_name = True

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize a new instance of the model.

        This method sets up the fields and attributes for the model instance,
        ensuring that the correct values are assigned and managing relationships.

        Args:
            *args (Any): Positional arguments for field values.
            **kwargs (Any): Keyword arguments for field values.

        Raises:
            IndexError: If the number of positional arguments exceeds the number
                        of fields.
        """
        opts: MetaOptions = self._meta
        if len(args) > len(opts.local_fields):
            raise IndexError("Number of args exceeds number of fields")

        fields_iter = iter(opts.local_fields)

        # args
        for val, field in zip(args, fields_iter):
            kwargs[field.name] = val

        # kwargs
        for field in fields_iter:
            if field.is_relation and field.column in kwargs:
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
            value = kwargs.get(field.column, None)
            object.__setattr__(self, field.column, value)
        self._changes: dict [str, str] = {}


    def _get_pk_val(self) -> Any:
        """Get the value of the primary key.

        Returns:
            Any: The value of the primary key.
        """
        return getattr(self, self._meta.primary_key.name)

    def _set_pk_val(self, value: Any) -> None:
        """Set the value of the primary key.

        Args:
            value (Any): The value to set as the primary key.
        """
        name = self._meta.primary_key.name
        setattr(self, name, value)

    pk = property(_get_pk_val, _set_pk_val)

    def __eq__(self, other: object):
        """Check equality between two model instances.

        Args:
            other (object): The object to compare with.

        Returns:
            bool: True if the objects are equal, False otherwise.
        """
        if not isinstance(other, Model):
            return NotImplemented
        if type(self) != type(other):
            return False
        my_pk = self.pk
        if my_pk is None:
            return self is other
        return my_pk == other.pk

    def __setattr__(self, name: str, value: Any) -> None:
        """Set an attribute value.

        Args:
            name (str): The name of the attribute.
            value (Any): The value to set.
        """
        if name not in self.__fields__: # type: ignore
            self.__fields__[name] = Field(default=None) # type: ignore
        super().__setattr__(name, value)
        if hasattr(self, '_changes') and name != '_changes' and name != '_session':
            self._changes[name] = value
            if hasattr(self, '_session'):
                self._session.changed(self) # type: ignore
        if name in self._meta.relation_fields_name():
            field = self._meta.get_relation_field(name)
            object.__setattr__(self, field.column, None)
        elif name in self._meta.relation_fields_column():
            field = self._meta.get_relation_field(name)
            object.__setattr__(self, field.name, None)

    def __getattribute__(self, name: str) -> Any:
        """Get an attribute value.

        Args:
            name (str): The name of the attribute.

        Returns:
            Any: The value of the attribute.
        """
        value = super().__getattribute__(name)

        # if atrr is relation and it is object
        if value is None and name in self._meta.relation_fields_name():
            field = self._meta.get_relation_field(name)
            if object.__getattribute__(self, field.column):
                if hasattr(self, '_session') and getattr(self, '_session'):
                    value = self._session.get(field.related_model, self.pk)
                    setattr(self, field.name, value)
                else:
                    raise ValueError("First add object to session!")
            # do not change if not id

        # if atrr is relation and it is id
        elif value is None and name in self._meta.relation_fields_column():
            field = self._meta.get_relation_field(name)
            if object.__getattribute__(self, field.name):
                value = object.__getattribute__(self, field.name).pk
        return value

    def _get_name_and_pk(self):
        """Get the table name and primary key value.

        Returns:
            tuple: The table name and primary key value.
        """
        return self._meta.db_table, self.pk

    def _get_attr_values(self) -> list[Any]:
        """Get a list of attribute values.

        Returns:
            list: A list of attribute values.
        """
        atrr_values : list[Any] = []
        for field in self._meta.local_fields:
            if field.is_relation:
                atrr_values.append((field.column, getattr(self, field.column)))
            else:
                value = getattr(self, field.name)
                if value is not None:
                    atrr_values.append((field.name, value))
        return atrr_values

    def _update_changes_db(self) -> dict[str, str]:
        """Update changes in the database.

        Returns:
            dict: A dictionary of changes.
        """
        changes = self._changes
        self._changes = {}
        return changes

    def _add_session(self, session: 'Session') -> None:
        """Add a session to the instance.

        Args:
            session (Session): The session to add.
        """
        self._session = session

    def _remove_session(self) -> None:
        """Remove the session from the instance."""
        self._session = None

    def _is_pk_none(self) -> bool:
        """Check if the primary key is None.

        Returns:
            bool: True if the primary key is None, False otherwise.
        """
        return self.pk is None and isinstance(self._meta.primary_key, AutoField)

    def _get_db_pk(self):
        """Get the database primary key value.

        Returns:
            tuple: The primary key column name and value.
        """
        return self._meta.primary_key.column, self.pk

    @classmethod
    def _get_primary_key_column(cls) -> str:
        return cls._meta.primary_key.column # type: ignore

    @classmethod
    def _get_columns_names(cls) -> list[str]:
        return [field.column for field in cls._meta.local_fields] # type: ignore