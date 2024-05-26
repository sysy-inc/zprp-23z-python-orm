from typing import Any, Dict, List
from pydantic import Field
import bisect
from skibidi_orm.query_engine.field.field import AutoField


class MetaOptions:
    """ A subsidiary to store additional information"""
    def __init__(self, meta: Dict[str, Any]):
        self.db_table = ''
        self.meta = meta
        self.primary_key = None
        self.local_fields: List[Any] = []

    def contribute_to_class(self, cls: Any, obj_name: str) -> None:
        """ Adds atrributes to classes """
        cls._meta = self
        self.model = cls

        db_table = self.meta['db_table'] if self.meta else cls.__name__.lower()
        self.db_table = db_table

    def add_field(self, field: Any):
        """ Adds database column """
        bisect.insort(self.local_fields, field)
        self.setup_pk(field)

    def setup_pk(self, field: Any):
        """ Setup the primary key """
        if self.primary_key and field.primary_key:
            # TODO raise error
            pass
        elif not self.primary_key and field.primary_key:
            self.primary_key = field

    def _prepare(self, model: Any):
        if not self.primary_key:
            obj_name = self.model.__name__.lower() + '_id'
            self.model.add_to_class(obj_name, AutoField(primary_key=True))
            self.model.__fields__[obj_name] = Field(default=None)