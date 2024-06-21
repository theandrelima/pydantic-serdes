import inspect
from collections import defaultdict
from functools import cache
from typing import TYPE_CHECKING, Any, DefaultDict, Dict, Optional, Type, Union

from pydantic_serdes.custom_collections import PydanticSerdesSortedSet
from pydantic_serdes.exceptions import (DataStoreDirectAssignmentError,
                                        ModelInstanceAlreadyExistsError,
                                        ModelInstanceDoesNotExistError,
                                        MultipleModelInstancesReturnedError)

if TYPE_CHECKING:
    from pydantic_serdes.models import PydanticSerdesBaseModel


class ModelsGlobalStore:
    """
    Implements a global store for all the models in the application.

    Models are stored in a defaultdict, where the keys are the model
    classes names and the values are PydanticSerdesSortedSet objects.

    The PydanticSerdesSortedSet is a custom collection that stores the
    models in a sorted order, based on the `key` attribute of the model.

    An example of how the structure looks like:
    {
        "Model1": PydanticSerdesSortedSet([Model1_instance1, Model1_instance2, ...]),
        "Model2": PydanticSerdesSortedSet([Model2_instance1, Model2_instance2, ...]),
        ...
    }

    Only one instance of this class is created, and it's shared across the
    entire application. This is done to ensure that all the models are stored
    in the same place and that they can be accessed from anywhere in the
    application. See the `get_global_data_store` function for more details.
    """

    _records = defaultdict(PydanticSerdesSortedSet)

    @property
    def records(
        self,
    ) -> DefaultDict[str, PydanticSerdesSortedSet]:
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

    def save(self, obj: "PydanticSerdesBaseModel") -> None:
        """
        Saves a model instance to the global store.

        If a key matching the object's class name is not in self.records, it will
        be added to the store and the model instance will be added to the
        PydanticSerdesSortedSet associated with that key.Otherwise, the model
        instance will be added to the existing obj.__class__ key.

        Args:
            obj (PydanticSerdesBaseModel): the PydanticSerdesBaseModel instance to be saved.

        Raises:
            ModelAlreadyExists: if the model instance is already in the store
            and the `_err_on_duplicate` attribute is set to True.
        """
        cls_name = self._get_cls_name(obj)

        if obj in self.records[cls_name] and obj._err_on_duplicate:
            raise ModelInstanceAlreadyExistsError(
                f"{cls_name}: duplicates not allowed. Make sure there's no other "
                f"{cls_name} with fields {obj._key} associated with values {obj.key}, respectively."
            )

        self.records[cls_name].add(obj)

    def _get_cls_name(
        self, obj: Union[Type["PydanticSerdesBaseModel"], "PydanticSerdesBaseModel"]
    ) -> str:
        """
        Returns the name of the class of the given object.

        Args:
            obj (Union[Type["PydanticSerdesBaseModel"], "PydanticSerdesBaseModel"]): could be
            either a class object or an instance of a class.

        Returns:
            str: the name of the class of the given object.
        """
        if inspect.isclass(obj):
            return obj.__name__

        return obj.__class__.__name__

    def _search(
        self,
        model_class: Type["PydanticSerdesBaseModel"],
        search_params: Optional[Dict[Any, Any]] = None,
    ) -> PydanticSerdesSortedSet:
        """
        Searches the records of a given model class based on the search_params.

        Args:
            model_class (Type["PydanticSerdesBaseModel"]): the class of the model to
            be searched.
            search_params (Optional[Dict[Any, Any]]): a dictionary with keys being the
            attributes of the model and the values being the values to be searched for.
            If `None`, returns the entire PydanticSerdesSortedSet associated with
            `model_class` key. Defaults to None.

        Returns:
            PydanticSerdesSortedSet: the PydanticSerdesSortedSet containing the records
            that match the search_params.
        """
        cls_name = self._get_cls_name(model_class)

        if search_params:
            return PydanticSerdesSortedSet(
                [
                    x
                    for x in self.records[cls_name]
                    if all(getattr(x, k) == v for k, v in search_params.items())
                ]
            )

        return self.records[cls_name]

    def filter(
        self,
        model_class: Type["PydanticSerdesBaseModel"],
        search_params: Dict[Any, Any],
    ) -> PydanticSerdesSortedSet:
        """
        Avails of self._search() to filter the records of a given model class
        based on the search_params.

        Args:
            model_class (Type["PydanticSerdesBaseModel"]): the class of the
            model to be filtered.
            search_params (Dict[Any, Any]): the search parameters to be used
            to filter the records.

        Returns:
            PydanticSerdesSortedSet: the PydanticSerdesSortedSet containing
            the records that match the search_params.
        """
        return self._search(model_class, search_params)

    def get(
        self,
        model_class: Type["PydanticSerdesBaseModel"],
        search_params: Dict[Any, Any],
    ) -> "PydanticSerdesBaseModel":
        """
        Avails of self.filter() method to get a single model instance from
        the global store based on the search_params.

        Args:
            model_class (Type["PydanticSerdesBaseModel"]): the class of the model
            to be filtered.
            search_params (Dict[Any, Any]): the search parameters to be used
            to filter the records.

        Raises:
            ModelDoesNotExist: if a PydanticSerdesBaseModel does not exist in
            the datastore matching the search_params.
            ModelAlreadyExists: if more than one PydanticSerdesBaseModel exists
            in the datastore matching the search_params.

        Returns:
            PydanticSerdesBaseModel: a single PydanticSerdesBaseModel instance.
        """
        search = self.filter(model_class, search_params)

        if not search:
            raise ModelInstanceDoesNotExistError(
                f"A {model_class.__name__} object was not found matching params: {search_params}"
            )

        if len(search) > 1:
            raise MultipleModelInstancesReturnedError("More than one element found")

        return search[0]

    def get_all_by_class(
        self, model_class: Type["PydanticSerdesBaseModel"]
    ) -> PydanticSerdesSortedSet:
        """
        Avails of self._search() method to get all the records of a given
        model class from the global store.

        Args:
            model_class (Type["PydanticSerdesBaseModel"]): the class of the model

        Returns:
            PydanticSerdesSortedSet: the PydanticSerdesSortedSet containing all the
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
