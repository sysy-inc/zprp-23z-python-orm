from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from skibidi_orm.query_engine.field.related_field import ForeignKey
    from skibidi_orm.query_engine.model.base import Model


class RelationObject:
    """
    Class for storing relation data.

    Attributes:
        field (ForeignKey): The foreign key field associated with the relation.
        model (str): The name of the target model.
        related_name (str): The optional related name for the relation.
    """

    def __init__(
        self,
        field: 'ForeignKey',
        to: 'Model',                        # target model
        related_name: str = "",
    ):
        """
        Initializes a new instance of the RelationObject class.

        Args:
            field (ForeignKey): The foreign key field associated with the relation.
            to (str): The name of the target model.
            related_name (str, optional): The optional related name for the relation.
        """
        self.field = field
        self.model = to
        self.related_name = related_name

