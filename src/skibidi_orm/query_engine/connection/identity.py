"""
Storage for model objects to ensure that only one instance of model is used
"""
from skibidi_orm.query_engine.model.base import Model
from typing import Any, Optional


class IdentityMap:
    def __init__(self) -> None:
        self._dict: dict[tuple[str, Any], Model | None] = {}

    def __len__(self) -> int:
        return len(self._dict)

    def __getitem__(self, key: tuple[str, Any]) -> Model:
        o = self._dict[key]
        if o is None:
            raise KeyError(key)
        return o

    def add(self, obj: Model) -> bool:
        # key = obj.key()   this function needs to be made in Model, returns (model_name, primary_key)
        key = ("test_model", 1)     # temporarly TOCHANGE
        if key in self._dict:
            # this key is already present
            existing_obj = self._dict[key]
            if existing_obj is not obj:
                # different instance saved with the same key
                if existing_obj is not None:
                    # TODO change to custom exception
                    raise Exception("Can't add this instance, another instance with this key is present")
            else:
                # this instance is already saved
                return False

        self._dict[key] = obj
        return True

    def get(self, key: tuple[str, Any], default: Optional[Model] = None) -> Optional[Model]:
        if key not in self._dict:
            return default
        obj = self._dict[key]
        if obj is None:
            return default
        return obj

    def remove(self, obj: Model) -> None:
        # key = obj.key()   this function needs to be made in Model, returns (model_name, primary_key)
        key = ("test_model", 1)     # temporarly TOCHANGE
        if key in self._dict:
            o = self._dict[key]
            if o is obj:
                self._dict.pop(key, None)
