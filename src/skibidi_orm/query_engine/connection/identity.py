"""
This module provides the IdentityMap class, which is responsible for managing a collection
of model instances to ensure that only one instance of each object exists within the application context.
"""
from skibidi_orm.query_engine.model.base import Model
from typing import Any, Optional


class IdentityMap:
    """
    Manages a collection of model instances to ensure that only one instance of each
    object exists within the application context.

    Attributes:
        _dict (dict[tuple[str, Any], Model | None]): A dictionary storing model instances,
            keyed by a tuple of model name and primary key.
    """
    def __init__(self) -> None:
        """
        Initializes the IdentityMap with an empty dictionary.
        """
        self._dict: dict[tuple[str, Any], Model | None] = {}

    def __len__(self) -> int:
        """
        Returns the number of entries in the identity map.

        Returns:
            int: The number of entries in the identity map.
        """
        return len(self._dict)

    def __getitem__(self, key: tuple[str, Any]) -> Model:
        """
        Retrieves the model instance associated with the given key.

        Args:
            key (tuple[str, Any]): The key to retrieve the model instance.

        Returns:
            Model: The model instance associated with the given key.

        Raises:
            KeyError: If the key is not found or the associated value is None.
        """
        o = self._dict[key]
        if o is None:
            raise KeyError(key)
        return o

    def __contains__(self, item: Model) -> bool:
        """
        Checks if the given model instance is in the identity map.

        Args:
            item (Model): The model instance to check.

        Returns:
            bool: True if the model instance is in the identity map, False otherwise.
        """
        return item._get_name_and_pk() in self._dict    # type: ignore

    def add(self, obj: Model) -> bool:
        """
        Adds a model instance to the identity map.

        Args:
            obj (Model): The model instance to add.

        Returns:
            bool: True if the model instance was added, False if it was already present.

        Raises:
            Exception: If a different instance with the same key is already present.
        """
        key = obj._get_name_and_pk()    # type: ignore
        if key in self._dict:
            # this key is already present
            existing_obj = self._dict[key]
            if existing_obj is not obj:
                # different instance saved with the same key
                if existing_obj is not None:
                    raise Exception("Can't add this instance, another instance with this key is present")
            else:
                # this instance is already saved
                return False

        self._dict[key] = obj
        return True

    def get(self, key: tuple[str, Any], default: Optional[Model] = None) -> Optional[Model]:
        """
        Retrieves the model instance associated with the given key, or returns the default value if not found.

        Args:
            key (tuple[str, Any]): The key to retrieve the model instance.
            default (Optional[Model]): The default value to return if the key is not found. Defaults to None.

        Returns:
            Optional[Model]: The model instance associated with the given key, or the default value if not found.
        """
        if key not in self._dict:
            return default
        obj = self._dict[key]
        if obj is None:
            return default
        return obj

    def remove(self, obj: Model) -> None:
        """
        Removes the given model instance from the identity map.

        Args:
            obj (Model): The model instance to remove.
        """
        key = obj._get_name_and_pk()    # type: ignore
        if key in self._dict:
            o = self._dict[key]
            if o is obj:
                self._dict.pop(key, None)
