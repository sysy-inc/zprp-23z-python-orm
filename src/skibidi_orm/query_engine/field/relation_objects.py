from skibidi_orm.query_engine.field.related_field import ForeignKey


class RelationObject:
    """
    Class for storing relation data 
    """
    def __init__(
        self,
        field: ForeignKey,
        to: str,                        # target model name
        related_name: str = "",
        on_delete: str = "",            # TODO implement proper deleting
    ):
        self.field = field
        self.model = to
        self.related_name = related_name
        self.on_delete = on_delete

    def set_field_name(self):
        self.field_name = self.model._meta.pk.name       # type: ignore
