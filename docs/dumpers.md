# SerialBus Dumpers
Should you ever wish to take data from your models back to a serialization format, you can do that by using a dumper 
function. A dumper takes a Python dictionary as input and returns the serialized data as a string. 

Because SerialBus models are pydantic models, you can convert them to Python dictionaries by calling either 
the `.dict()` or the `.model_dump()` methods on an instance of a model before passing it to a dumper function. 
Additionally, you can dump your entire global data store to a serialized format by calling the `.as_dict()` method 
on the `GLOBAL_DATA_STORE` object. This will return a dictionary with all previously loaded data, which you can then 
pass to a dumper function.

It is worth mentioning that by means of loader and dumper functions, you could easily convert data from one format to
another by availing of the [`utils.convert_src_file_to()`](/serial_bus/utils.py) function (as seen in 
[Converting data between supported formats](/docs/getting_started.md#example-3-converting-data-between-supported-formats)).


## Built-in Dumpers
The [`serial_bus/dumpers.py`](/serial_bus/dumpers.py) module is where the built-in dumper 
functions provided by SerialBus live, supporting common data formats such as JSON, YAML, TOML, and 
INI.

Because SerialBus was designed to be extensible, it is possible to add support for other file formats by 
creating your own custom dumper functions.

## How to Create Custom Dumper Functions?

If your project requires different file formats or specific serialization logic, you can create custom dumper 
functions to meet these needs, following these conventions:

- for each output format you want to support, create a separate dumper function and include the serialization format 
  in its respective function name, following the pattern:`{format}_dumper`. For example, a custom dumper function 
  for JSON data must be named `json_dumper`.


- the function(s) should receive an argument representing the input dict and return the serialized data as a string.


- the function(s) should be placed in a module, and the module's dotted path should be set in the `DUMPERS_MODULE` 
  environment variable. For example, if your project's package is named 'my_package' and you created custom dumper 
  function(s) in a module named 'my_dumpers.py' you should set the `DUMPERS_MODULE` environment variable to 
  `my_package.my_dumpers`.

Users are encouraged to look at [dumpers.py](/serial_bus/dumpers.py) to get an idea of how a dumper function 
*COULD* be implemented. However, as long as the function is capable of writing to a particular serialized format and 
returning a string, the actual implementation matters little (except for the conventions mentioned above).