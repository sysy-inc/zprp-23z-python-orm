""" A model class for mapping database table """

from pydantic import BaseModel
from pydantic.main import ModelMetaclass
from typing import Any, Tuple, Dict



class MetaModel(ModelMetaclass):
    """ A metaclass for model """
    def __new__(cls, name: str, bases: Tuple[Any], attrs: Dict[str, Any]) -> Any:
        super_new: Any = super().__new__ # type: ignore
        # TODO check if name is correct
        # TODO check if attrs' names are correct
        # TODO check if is primary key
        # TODO check if only one attr is primary key
        # TODO check if atrr db_column is unique
        return super_new(cls, name, bases, attrs)




class Model(BaseModel):
    """ A class to create your own database table """
    # TODO add information about inheritance
    pass