""" A model class for mapping database table """

from pydantic import BaseModel
from pydantic.main import ModelMetaclass




class MetaModel(ModelMetaclass):
    """ A metaclass for model """
    pass



class Model(BaseModel, metaclass=MetaModel):
    """ A class to create your own database table """
    # TODO add information about inheritance
    pass