from sortedcontainers import SortedSet


class HashableDict(dict):
    """
    A ridiculously simple implementation of a hashable dictionary.

    All fields in a serial_weaver model must be hashable so that the model
    instance itself can be hashable as well. Because Python's native dict
    is not hashable, this class might come in handy for serial_weaver model
    fields that have to be dicts.

    Optionally, a code using serial_weaver may use its own implementation of a
    hashable dictionary through 'HASHABLE_DICT_MODULE' and 'HASHABLE_DICT_CLASS'
    environment variables. See serial_weaver.config.SerialWeaverConfig
    class for more details.

    NOTE: The requirement for a hashable dictionary is due to the fact that each
    model instance will be stored in a set data structure, implemented by the
    SerialWeaverSortedSet class.
    """

    def __hash__(self):
        return hash((frozenset(self), frozenset(self.values())))


class SerialWeaverSortedSet(SortedSet):
    """This class implements a custom SortedSet with the 'key' argument
    set to a function that returns a model object's `key` property.

    NOTE: the `key` property returns a tuple containing the values associated
    with attribute names found in the private `_key` field of a model object.
    For more details, look at serial_weaver.models.SerialWeaverBaseModel
    class and sortedcontainers.SortedSet class.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(key=lambda model_obj: model_obj.key, *args, **kwargs)
