"""
Module handles managing additional information for the database model.
"""

from typing import Any
from pydantic import Field
import bisect
from skibidi_orm.query_engine.field.field import AutoField


class MetaOptions:
    """A subsidiary to store additional information.

    This class stores meta information related to a database model, including
    table name, primary key, local fields, and relation fields.
    """

    def __init__(self, meta: dict[str, Any]) -> None:
        """Initializes a MetaOptions instance.

        Args:
            meta (Dict[str, Any]): A dictionary containing meta information.
        """
        self.db_table = ''
        self.meta = meta
        self.primary_key: Any = None
        self.local_fields: list[Any] = []
        self.relation_fields: list[Any] = []

    def contribute_to_class(self, cls: Any, obj_name: str) -> None:
        """Adds attributes to classes.

        This method adds the `_meta` attribute to the class and assigns
        it to the current instance. It also sets the `model` attribute of
        the instance to the class. Additionally, it sets the `db_table`
        attribute based on the `meta` attribute of the instance or defaults
        to the lowercase name of the class.

        Args:
            cls (Any): The class to which attributes are being added.
            obj_name (str): The name of the object.

        """
        setattr(cls, obj_name, self)
        self.model = cls

        db_table = self.meta['db_table'] if self.meta else cls.__name__.lower()
        self.db_table = db_table

    def add_field(self, field: Any) -> None:
        """Adds a database column.

        This method inserts the given field into the `local_fields` list
        while maintaining order. It also calls the `setup_pk` method to
        handle primary key setup. If the field represents a relationship,
        it is also inserted into the `relation_fields` list in order.

        Args:
            field (Any): The database field to be added.

        """
        bisect.insort(self.local_fields, field)
        self.setup_pk(field)
        if field.is_relation:
            bisect.insort(self.relation_fields, field)

    def setup_pk(self, field: Any) -> None:
        """Sets up the primary key for the model.

        This method ensures that the model has only one primary key. If the
        model already has a primary key and another field is marked as the
        primary key, an error is raised. If the model does not have a primary
        key and the field is marked as the primary key, the field is set as
        the primary key.

        Args:
            field (Any): The database field to be checked and potentially
                set as the primary key.

        Raises:
            ValueError: If the model already has a primary key and another
                field is marked as the primary key.
        """
        if self.primary_key and field.primary_key:
            raise ValueError('Model cannot have two primary key!')
        elif not self.primary_key and field.primary_key:
            self.primary_key = field

    def get_field_name(self, name: str) -> Any:
        """
        Retrieve a field by its name or column name.

        This method searches through the local fields of the instance to find a field that matches the given name
        or column name.

        Args:
            name (str): The name or column name of the field to search for.

        Returns:
            The field if found, otherwise None.
        """
        for field in self.local_fields:
            if field.name == name or field.column == name:
                return field
        return None

    def _prepare(self, model: Any) -> None:
        """Prepares the model for database interaction.

        This method checks if the model has a primary key defined. If not,
        it automatically adds an `AutoField` as the primary key and a
        corresponding field with default value None to the model.

        Args:
            model (Any): The model to be prepared for database interaction.
        """
        if not self.primary_key:
            obj_name = model.__name__.lower() + '_id'
            model.add_to_class(obj_name, AutoField(primary_key=True))
            model.__fields__[obj_name] = Field(default=None)

    def relation_fields_name(self) -> list[Any]:
        """Returns the names of the fields representing relationships.

        This method retrieves the names of the fields in the `relation_fields`
        list, which represent relationships with other models.

        Returns:
            List[str]: A list containing the names of the fields representing
                relationships.
        """
        return [field.name for field in self.relation_fields]

    def get_relation_field(self, name: str) -> Any:
        """Retrieves a field representing a relationship by its name or column name.

        This method searches for a field representing a relationship within the
        `relation_fields` list by comparing either the field name or the column
        name with the provided `name`. If a matching field is found, it is returned.

        Args:
            name (str): The name or column name of the field representing the
                relationship.

        Returns:
            Any: The field representing the relationship if found, otherwise None.
        """
        for field in self.relation_fields:
            if field.name == name or field.column == name:
                return field
        return None

    def relation_fields_column(self) -> list[Any]:
        """Returns the column names of the fields representing relationships.

        This method retrieves the column names of the fields in the
        `relation_fields` list, which represent relationships with other models.

        Returns:
            List[str]: A list containing the column names of the fields
                representing relationships.
        """
        return [field.column for field in self.relation_fields]

