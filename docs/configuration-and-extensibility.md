# Configuration & Extensibility

## PydanticSerdesConfig
The [**PydanticSerdesConfig**](/pydantic_serdes/config.py) class manages the configuration of pydantic-serdes. 
The class exposes a number of properties, each representing a configuration. Some of these configurations have a 
direct mapping to environment variables, and by setting them, you can customize the behavior of pydantic-serdes to 
suit your needs. Some other configs won't have a direct mapping to an environment variable, but will be processed 
based on the state of configs that do.

Let's start with the configurations that you can directly set through environment variables.

| Config | Environment Var | Description                                                                                                                                                                                                                                                                                                                                                                                                      | Default Value |
| --- | --- | --- | --- |
| `models_modules` ❗ | `MODELS_MODULES` | It's a comma-separated string of Python dotted paths to modules containing subclasses of `PydanticSerdesBaseModel` or `PydanticSerdesRenderableModel`. *This config is of central importance to pydantic-serdes. See more about it below.*                                                                                                                                                                  | `"pydantic_serdes.models"` |
| `template_dir` | `TEMPLATES_DIR` | The directory where Jinja2 template files mapping to `PydanticSerdesRenderableModel` subclasses will exist.                                                                                                                                                                                                                                                                                                    | `"templates"` |
| `hashable_dict_cls` | `HASHABLE_DICT_CLS` | The python dotted path to a class that implements hashable dictionaries. Check [custom_collections.HashableDict()](/pydantic_serdes/custom_collections.py) for the default implementation provided with this package. If you want to do something different, you must set this ENV var pointing to your custom implementation.                                                                                 | `"pydantic_serdes.custom_collections.HashableDict"`|
| `loaders_module` | `LOADERS_MODULE` | The python dotted path to the module providing loader functions. If you want to support loading from formats that are not supported yet, or include custom parsing logic, this is the ENV var you need to set to your own python module. Check [pydantic_serdes.loaders.py](/pydantic_serdes/loaders.py) to see how a loader function should behave.                                                         | `"pydantic_serdes.loaders"`|
| `dumpers_module` | `DUMPERS_MODULE` | Python dotted path to the module providing dumper functions. If you want to support dumping to formats that are not supported yet, or include custom parsing business logic to you dumping process, this is the ENV var you need to set with the path to your module with your dumper functions. Check [pydantic_serdes.dumpers.py](/pydantic_serdes/dumpers.py) to see how a dumper function should behave. | `"pydantic_serdes.dumpers"`|

Other 2 important configs that don't have a direct mapping to an environment variable but will be indirectly influenced
by some of the configs above are:

| Config | Description                                                                                                                                                                                                                                                                                                                                                                                                                               | Default Value            |
| --- | --- | --- |
| `supported_formats` | A list of strings representing the file formats that are supported for loading. This will be inferred from all loader functions taken from the `loaders_module` config. For simplicity, we only take loaders as the basis to determine the supported formats.                                                                                                                                                                             | -                        |
| `directive_to_model_mapping`❗ | Also a crucial config. This is a dictionary with the directive names as keys and the Model Classes themselves as values. This config will be processed when pydantic-serdes accesses it for the first time, which will happen when it first attempts to instantiate models. Once processed it never changes. It can be influenced by the `models_module` config, if it has any value set through `MODELS_MODULES` ENV var. | An empty dictionary - {} |

As mentioned above, of special importance is the `models_module` config, set through `MODELS_MODULES` ENV var. The 
reason for it is that it will have a direct impact on the processing of the `directive_to_model_mapping` config. 
Here is what you have to understand about the `directive_to_model_mapping` config:

1. the `PydanticSerdesBaseModel` class has a registry for all of its subclasses. As soon as the python 
   interpreter imports anything from a module that contains a subclass of `PydanticSerdesBaseModel`, it registers 
   that subclass within `PydanticSerdesBaseModel._subclasses` attribute.
2. when pydantic-serdes tries to instantiate model classes for the first time, it will inspect the 
   `directive_to_model_mapping` config, which
in turn will trigger an import of all modules listed in the `models_module` config (`MODELS_MODULES` env var). This 
   is to enforce the registry mentioned in 1 to be populated.
3. right after trying to import all modules in `MODELS_MODULES`, the code will then examine 
   `PydanticSerdesBaseModel._subclasses` to filter out only those subclasses that have the `_directive` attribute 
   set to some string value. This value will become a key in the `directive_to_model_mapping` dictionary, while the 
   class itself will be the associated value of that key. 

When 3 above happens, it's crucial that all your model classes must have been imported by the python interpreter 
already, otherwise they would not have been registered in `PydanticSerdesBaseModel._subclasses`. And because this 
lookup is only ever triggered once, whatever it returns will be the forever value of `directive_to_model_mapping` 
config. And that's why **it's encouraged that you always avail of `MODELS_MODULES` env var**, as it will explicitly 
instruct pydantic_serdes on where to look for classes that inherit from one of it's base models. 
