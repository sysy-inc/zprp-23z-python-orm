from skibidi_orm.query_engine.field.field import Field, IntegerField
from skibidi_orm.query_engine.field.relation_objects import RelationObject
from typing import Any, Type, Union


def get_field(x: str):
    return Field()


class ForeignKey(Field):
    """Base class that all relational fields inherit from."""

    one_to_many = False
    one_to_one = False
    many_to_many = False
    many_to_one = False

    def __init__(
        self,
        to: str,
        on_delete: str,
        # to_fields: list[str],
        rel: Union[RelationObject, None] = None,
        related_name: str = "",
        **kwargs: Any
    ):

        if rel is None:
            rel = RelationObject(
                self,
                to,
                related_name=related_name,
                on_delete=on_delete,
            )

        super().__init__(
            related=rel,
            **kwargs
        )

        self.related_name = related_name,
        # self.to_fields = to_fields

    @property
    def related_model(self):
        return self.remote_field.model
    
    # TODO add checks

    def contribute_to_class(self, cls: Type[BaseException], name: str):
        super().contribute_to_class(cls, name)
        # TODO what needs to be added here?

    def set_attributes_from_rel(self):
        self.name = self.name or (
            self.remote_field.model._meta.model_name
            + "_"
            + self.remote_field.model._meta.pk.name
        )
        self.remote_field.set_field_name()


field1 = IntegerField()
field2 = ForeignKey(to='nazwamodelu', on_delete='cos')