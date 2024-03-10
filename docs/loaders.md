# Serial Weaver Loaders
Loader functions play a crucial role in the Serial Weaver framework by enabling the conversion of serialized 
data into Python dictionaries, which can then be used to create instances of Serial Weaver models. The process 
works as follows:  
 - The loader function reads serialized data from a source, which could be a file or a TextIO object. 


 - The loader function then parses this serialized data and converts it into a Python dictionary. This process is known
   as deserialization.


 - Once the data is deserialized into a Python dictionary, it can be used to create an instance of a 
   Serial Weaver model. This is because Serial Weaver models are essentially Pydantic models, which can be 
   instantiated using Python dictionaries. 


 - The instantiated model(s) can then be used in the application, with all the benefits of pydantic's 
runtime type checking and data validation.

It's also worth mentioning that when you use [utils.generate_from_file()](/serial_weaver/utils.py),
this process is done automatically for you. Serial Weaver will select the appropriate loader function based on the 
file extension and then use it to create instances of your model(s), as seen in [Instantiating models from 
serialized data](/docs/getting_started.md#example-1-instantiating-models-from-serialized-data).

## Built-in Loaders

The [`serial_weaver/loaders.py`](/serial_weaver/loaders.py) module is where the built-in loader functions 
provided by Serial Weaver framework live. 

The loader functions shipped with Serial Weaver can handle different types of input sources, including file paths 
and TextIO objects. They are designed to be flexible with built-in support for common data formats such
as JSON, YAML, TOML, and INI.

Because Serial Weaver was designed to be extensible, it is possible to add support for other file formats by
creating your own custom loader functions.


## How to Create Custom Loader Functions?

If your project requires different file formats or specific deserialization logic, you can create 
custom loader functions to meet these needs. For total coupling with Serial Weaver's nice features (like 
automatic loader selection) some conditions have to be met:

- for each format you want to support, create a separate loader function and include the serialization format in its 
  respective function name, following the pattern:`{format}_loader`. For example, a custom loader function for 
  JSON data must be named `json_loader`.


- the function(s) should receive an argument representing the input data and return the deserialized data as a Python 
  dictionary.


- the function(s) should be placed in a module, and the module's dotted path should be set in the `LOADERS_MODULE` 
  environment variable. For example, if your project's package is named 'my_package' and you created custom loader 
  function(s) in a module named 'my_loaders.py' you should set the `LOADERS_MODULE` environment variable to 
  `my_package.my_loaders`.

Users are encouraged to look at [loaders.py](/serial_weaver/loaders.py) to get an idea of how a loader function 
*COULD* be implemented. However, as long as the function is capable of reading from a particular serialized format and 
returning a python dict, the actual implementation matters little (except for the conventions mentioned above). 
