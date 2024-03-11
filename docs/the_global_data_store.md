# The GLOBAL_DATA_STORE
> *OBS: this section is technically detailed and is provided for the sake of completeness. Its reading is not 
> crucial for being able to use SerialBus, but might help gaining a more complete understanding of the
> tool as a whole.*

`GLOBAL_DATA_STORE` is a global scope variable found in [datastore.py](/serial_bus/datastore.py) module that 
is intended to hold a single instance of the `ModelsGlobalStore` class, also found in the same module. This instance 
is meant to be shared across the entire application, providing a centralized place to store and access model instances.

The `GLOBAL_DATA_STORE` is initially set to `None`. It is not assigned an instance of `ModelsGlobalStore` directly 
in the global scope. Instead, it is assigned a value when `get_global_data_store` function is called.

The `get_global_data_store` function is decorated with `functools.cache`, which means it will cache its result after 
the first call. Here is how it works:
- The first time `get_global_data_store` is called, it checks if `GLOBAL_DATA_STORE` is None. 
- If it is, it creates a new `ModelsGlobalStore` instance and assigns it to `GLOBAL_DATA_STORE`.
- For all later calls, it immediately returns `GLOBAL_DATA_STORE`.

This singleton pattern ensures that there is only one `ModelsGlobalStore` instance in the application, and it can be 
accessed by calling `get_global_data_store`.

## The `ModelsGlobalStore` class
The `ModelsGlobalStore` class is designed to be a global store for all models in the application. It uses a 
defaultdict to store models, where the keys are the model class names and the values are [SerialBusSortedSet](/serial_bus/custom_collections.py) objects. The `SerialBusSortedSet` is a custom collection that 
stores the models in a sorted order, based on the `key` property of the model, which in turn simply returns all 
values associated with each attribute namely defined by the tuple of strings in the `._key` attribute of the model 
class.

Here's a breakdown of its attributes and methods:

- `_records`: This is a defaultdict that stores the models. It's initialized with `SerialBusSortedSet` as the 
  default factory function, so any new keys will automatically be assigned an empty `SerialBusSortedSet`.

- `records`: This is a property that provides access to `_records`. It has a getter and a setter. The getter simply 
  returns `_records`. The setter raises a `DataStoreDirectAssignmentError` if you try to assign to records directly, 
  preventing modification of the entire data store directly.

- `as_dict()`: This method returns a regular Python dictionary version of the `records` attribute. It iterates over 
  records, and for each key-value pair, it creates a new key-value pair where the key is the same and the value is a 
  list of the results of calling `pydantic.BaseModel.model_dump()` on each record in the value.

- `save(obj)`: This method saves a model instance to the global store. It first checks if the object is already in 
  the store and raises a `ModelInstanceAlreadyExistsError` if it is and the object's `_err_on_duplicate` attribute is True. 
  Otherwise, it adds the object to the appropriate `SerialBusSortedSet` in `_record` defaultdict.

- `_get_cls_name(obj)`: This private method returns the object's class name. It checks if the object is a class or 
  an instance and returns the appropriate name.

- `_search(model_class, search_params)`: This private method searches the records of a given model class based on 
  the search_params. If search_params is provided, it returns a `SerialBusSortedSet` of records where the 
  attribute specified by search_params matches the value. If search_params is not provided, it returns all records 
  of the given model class.

- `filter(model_class, search_params)`: This method uses `_search()` to filter the records of a given model class 
  based on the search_params and returns the result.

- `get(model_class, search_params)`: This method uses `filter()` to get a single model instance from the global store 
  based on the search_params. It raises a `ModelInstanceDoesNotExistError` if no matching model is found, and a 
  `MultipleModelInstancesReturnedError` if more than one matching model is found.

- `get_all_by_class(model_class)`: This method uses `_search()` to get all the records of a given model class from 
  the global store. It does not require any search parameters. 


In summary, `ModelsGlobalStore` provides a global, sorted store for models. It provides methods to add models to the 
store, and to search for and retrieve models from the store based on their attributes. The store is implemented as a 
defaultdict of `SerialBusSortedSet` objects, ensuring that each set of models of the same class is kept in 
sorted order.