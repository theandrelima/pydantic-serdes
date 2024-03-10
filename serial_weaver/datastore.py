import inspect
from collections import defaultdict
from functools import cache
from typing import TYPE_CHECKING, Any, DefaultDict, Dict, Optional, Type, Union

from serial_weaver.custom_collections import SerialWeaverSortedSet
from serial_weaver.exceptions import (
    DataStoreDirectAssignmentError,
    ModelAlreadyExistsError,
    ModelDoesNotExistError,
)

if TYPE_CHECKING:
    from serial_weaver.models import SerialWeaverBaseModel


class ModelsGlobalStore:
    """
    Implements a global store for all the models in the application.

    Models are stored in a defaultdict, where the keys are the model
    classes names and the values are SerialWeaverSortedSet objects.

    The SerialWeaverSortedSet is a custom collection that stores the
    models in a sorted order, based on the `key` attribute of the model.

    An example of how the structure looks like:
    {
        "Model1": SerialWeaverSortedSet([Model1_instance1, Model1_instance2, ...]),
        "Model2": SerialWeaverSortedSet([Model2_instance1, Model2_instance2, ...]),
        ...
    }

    Only one instance of this class is created, and it's shared across the
    entire application. This is done to ensure that all the models are stored
    in the same place and that they can be accessed from anywhere in the
    application. See the `get_global_data_store` function for more details.
    """

    _records = defaultdict(SerialWeaverSortedSet)

    @property
    def records(
        self,
    ) -> DefaultDict[str, SerialWeaverSortedSet]:
        return self._records

    @records.setter
    def records(self, _):
        raise DataStoreDirectAssignmentError(
            "Cannot directly assign to attribute 'records' of a ModelsGlobalStore object."
        )

    def as_dict(self) -> Dict[str, Any]:
        """
        Returns regular python dict version of the records attribute.
        This makes it more human-friendly, as well easier to serialize the
        records attribute to a file by using any of the dumper functions in
        the dumpers module.
        """

        dump = {}

        for key, value in self.records.items():
            dump[key] = [record.model_dump() for record in value]

        return dump

    def save(self, obj: "SerialWeaverBaseModel") -> None:
        """
        Saves a model instance to the global store.

        If a key matching the object's class name is not in self.records, it will
        be added to the store and the model instance will be added to the
        SerialWeaverSortedSet associated with that key.Otherwise, the model
        instance will be added to the existing obj.__class__ key.

        Args:
            obj (SerialWeaverBaseModel): the SerialWeaverBaseModel instance to be saved.

        Raises:
            ModelAlreadyExists: if the model instance is already in the store
            and the `_err_on_duplicate` attribute is set to True.
        """
        cls_name = self._get_cls_name(obj)

        if obj in self.records[cls_name] and obj._err_on_duplicate:
            raise ModelAlreadyExistsError(
                f"{cls_name}: duplicates not allowed. Make sure there's no other "
                f"{cls_name} with fields {obj._key} associated with values {obj.key}, respectively."
            )

        self.records[cls_name].add(obj)

    def _get_cls_name(self, obj: Union[Type["SerialWeaverBaseModel"], "SerialWeaverBaseModel"]) -> str:
        """
        Returns the name of the class of the given object.

        Args:
            obj (Union[Type["SerialWeaverBaseModel"], "SerialWeaverBaseModel"]): could be 
            either a class object or an instance of a class.

        Returns:
            str: the name of the class of the given object.
        """
        if inspect.isclass(obj):
            return obj.__name__
        
        return obj.__class__.__name__

    def _search(
        self,
        model_class: Type["SerialWeaverBaseModel"],
        search_params: Optional[Dict[Any, Any]] = None,
    ) -> SerialWeaverSortedSet:
        """
        Searches the records of a given model class based on the search_params.
        Currently, only one k:v pair is supported in the search_params.

        Args:
            model_class (Type["SerialWeaverBaseModel"]): the class of the model to
            be searched. 
            search_params (Optional[Dict[Any, Any]], optional): a single k:v pair
            dictionary with the key being the attribute of the model and the value
            being the value to be searched for. If None, returns the entire
            SerialWeaverSortedSet associated with model_class key. Defaults to None.

        Returns:
            SerialWeaverSortedSet: the SerialWeaverSortedSet containing the records
            that match the search_params.
        """
        cls_name = self._get_cls_name(model_class)

        if search_params:
            # we only take the first k,v pair from search_params
            search_k, value = list(search_params.items())[0]
            return SerialWeaverSortedSet(
                [x for x in self.records[cls_name] if getattr(x, search_k) == value]
            )

        return self.records[cls_name]

    def filter(
        self,
        model_class: Type["SerialWeaverBaseModel"],
        search_params: Dict[Any, Any],
    ) -> SerialWeaverSortedSet:
        """
        Avails of self._search() to filter the records of a given model class
        based on the search_params. Currently, only one k:v pair is supported
        in the search_params.

        Args:
            model_class (Type["SerialWeaverBaseModel"]): the class of the
            model to be filtered.
            search_params (Dict[Any, Any]): the search parameters to be used
            to filter the records.

        Returns:
            SerialWeaverSortedSet: the SerialWeaverSortedSet containing
            the records that match the search_params.
        """
        return self._search(model_class, search_params)

    def get(
        self,
        model_class: Type["SerialWeaverBaseModel"],
        search_params: Dict[Any, Any],
    ) -> "SerialWeaverBaseModel":
        """
        Avails of self.filter() method to get a single model instance from
        the global store based on the search_params.

        Currently, only one k:v pair is supported in the search_params.

        Args:
            model_class (Type["SerialWeaverBaseModel"]): the class of the model
            to be filtered.
            search_params (Dict[Any, Any]): the search parameters to be used
            to filter the records.

        Raises:
            ModelDoesNotExist: if a SerialWeaverBaseModel does not exist in
            the datastore matching the search_params.
            ModelAlreadyExists: if more than one SerialWeaverBaseModel exists
            in the datastore matching the search_params.

        Returns:
            SerialWeaverBaseModel: a single SerialWeaverBaseModel instance.
        """
        search = self.filter(model_class, search_params)

        if not search:
            raise ModelDoesNotExistError(
                f"A {model_class.__name__} object was not found matching params: {search_params}"
            )

        if len(search) > 1:
            raise ModelAlreadyExistsError("More than one element found")

        return search[0]

    def get_all_by_class(
        self, model_class: Type["SerialWeaverBaseModel"]
    ) -> SerialWeaverSortedSet:
        """
        Avails of self._search() method to get all the records of a given
        model class from the global store.

        Args:
            model_class (Type["SerialWeaverBaseModel"]): the class of the model

        Returns:
            SerialWeaverSortedSet: the SerialWeaverSortedSet containing all the
            records of the given model class.
        """
        return self._search(model_class)


GLOBAL_DATA_STORE = None


@cache
def get_global_data_store():
    """
    Returns the shared instance of the ModelsGlobalStore. It's a cached function,
    meaning that it will only be executed once and the result will be stored in memory.
    This is done to ensure that the same instance of the class is returned every time
    the function is called.
    """

    global GLOBAL_DATA_STORE

    if GLOBAL_DATA_STORE is None:
        GLOBAL_DATA_STORE = ModelsGlobalStore()

    return GLOBAL_DATA_STORE
