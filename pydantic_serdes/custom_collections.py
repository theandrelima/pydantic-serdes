from collections.abc import Sequence
from typing import Generic, Tuple, TypeVar

from sortedcontainers import SortedSet

T = TypeVar("T")


class OneToMany(Tuple[T, ...], Generic[T]):
    """
    This class is provided as a means to map One-to-Many relationships between two model objects.

    It is nothing but a custom tuple subclass that enforces certain constraints on its elements:
        - The input iterable must be a sequence.
        - The sequence must not be empty.
        - All elements in the sequence must be of the same type.
        - Each element in the sequence must be hashable.

    If any of these constraints are not met, the class raises an appropriate error.

    Raises:
        TypeError: If the input is not a sequence, if the elements are not of the same type, or if an element
        is not hashable.
        ValueError: If the sequence is empty.

    Note:
        This class uses the `__new__` method for initialization, following the immutability principle of the
        tuple superclass.
    """

    def __new__(cls, iterable):
        if not isinstance(iterable, Sequence):
            raise TypeError(
                f"The OneToMany initialization iterable must be a sequence, but got {type(iterable).__name__}"
            )

        # Check if the sequence is non-empty
        if not iterable:
            raise ValueError("The OneToMany initialization iterable can't be empty")

        # Check if all elements are of the same type
        first_type = type(iterable[0])
        if not all(isinstance(item, first_type) for item in iterable):
            raise TypeError(
                "All elements of a OneToMany initialization iterable must be of the same type"
            )

        # Check if each element in the sequence is hashable
        for item in iterable:
            try:
                hash(item)
            except TypeError:
                raise TypeError(
                    f"Each element in the OneToMany initialization iterable must be hashable, but {item} isn't."
                )

        return super().__new__(cls, iterable)


class HashableDict(dict):
    """
    A ridiculously simple implementation of a hashable dictionary.

    All fields in a pydantic-serdes model must be hashable so that the model
    instance itself can be hashable as well. Because Python's native dict
    is not hashable, this class might come in handy for pydantic-serdes model
    fields that have to be dicts.

    Optionally, a code using pydantic-serdes may use its own implementation of a
    hashable dictionary by informing it using the 'HASHABLE_DICT_CLS'
    environment variable. See pydantic_serdes.config.PydanticSerdesConfig
    class for more details.

    NOTE: The requirement for a hashable dictionary is due to the fact that each
    model instance will be stored in a set data structure, implemented by the
    PydanticSerdesSortedSet class.
    """

    def __hash__(self):
        return hash((frozenset(self), frozenset(self.values())))


class PydanticSerdesSortedSet(SortedSet):
    """
    This class implements a custom SortedSet with the 'key' argument
    set to a function that returns a model object's `key` property.

    NOTE: the `key` property returns a tuple containing the values associated
    with attribute names found in the private `_key` field of a model object.
    For more details, look at pydantic_serdes.models.PydanticSerdesBaseModel
    class and sortedcontainers.SortedSet class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(key=lambda model_obj: model_obj.key, *args, **kwargs)
