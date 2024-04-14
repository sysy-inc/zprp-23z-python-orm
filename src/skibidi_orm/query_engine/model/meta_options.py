from typing import Any, Dict, List
import bisect


class MetaOptions:
    """ A subsidiary to store additional information"""
    def __init__(self, meta: Dict[str, Any]):
        self.db_table = meta['db_table']
        self.meta = meta
        self.primary_key = None
        self.local_fields: List[Any] = []

    def contribute_to_class(self, cls: Any, obj_name: str) -> None:
        """ Adds atrributes to classes """
        cls._meta = self
        self.model = cls

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
        # TODO check if attrs' names are correct
        # TODO check if is primary key
        # TODO check if atrr db_column is unique
        pass