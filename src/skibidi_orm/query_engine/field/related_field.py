from skibidi_orm.query_engine.field.field import Field
from skibidi_orm.query_engine.field.relation_objects import RelationObject
from typing import Any, Union, Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skibidi_orm.query_engine.model.base import Model


class ForeignKey(Field):
    """
    Represents a foreign key field.
    """
    def __init__(
        self,
        to: Union['Model', str],
        rel: Optional[RelationObject] = None,
        related_name: str = "",
        **kwargs: Any
    ):
        """
        Args:
            to (Model): The target model of the foreign key.
            rel (Union[RelationObject, None], optional): The relation object associated with the foreign key.
                Defaults to None.
            related_name (str, optional): The related name for the relation. Defaults to "".
            **kwargs (Any): Additional keyword arguments passed to the Field constructor.

        Attributes:
            related_name (str): The related name for the relation.
        """
        self.to = to
        self.rel = rel
        self.related_name = related_name
        super().__init__(**kwargs)

    @property
    def related_model(self):
        """
        Returns the related model associated with the remote field.

        Returns:
            (Model): The related model.
        """
        return self.remote_field.model
    
    def contribute_to_class(self, cls: 'Model', name: str):
        """
        Contributes the field to the class.
        """
        if self.to == 'self':
            self.to = cls  # Referencing the current class
        self.is_relation = True
        if self.rel is None:
            self.remote_field = RelationObject(
                self,
                self.to,  # type: ignore
                related_name=self.related_name
            )
        else:
            self.remote_field = self.rel

        super().contribute_to_class(cls, name)
        self.set_attributes_from_rel()

    def set_attributes_from_rel(self):
        """
        Sets attributes based on the related model.

        Sets the name attribute to a combination of the related model's model name and primary key name, 
        if not already set. Sets the column attribute to the name attribute appended with '_id', 
        if not already set.

        """
        self.name = self.name or (
            self.remote_field.model._meta.model_name
            + "_"
            + self.remote_field.model._meta.pk.name
        )
        self.column = self.name + "_id" or (
            self.remote_field.model._meta.model_name
            + "_"
            + self.remote_field.model._meta.pk.name
            + "_id"
        )

    @staticmethod
    def get_instance_by_name(name: str):
        """
        Retrieves an instance by its name from the global namespace.
        Args:
            name (str): The name of the instance to retrieve.
        Returns:
            Any: The instance associated with the given name.
        Raises:
            NameError: If an instance with the specified name does not exist in the global namespace.
        """
        if name in globals():
            return globals()[name]
        else:
            raise NameError(f"Instance with name '{name}' does not exist.")
    