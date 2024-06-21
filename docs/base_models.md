# pydantic-serdes Base Models

## [PydanticSerdesBaseModel](/pydantic_serdes/models.py)

>***Note**: The `PydanticSerdesBaseModel` class is not meant to be directly instantiated. Instead, it should be
>subclassed to create model classes.*

The `PydanticSerdesBaseModel` class is a foundational class that provides a lot of functionality for managing 
model instances. It ensures that instances are created, stored, and retrieved in a controlled and efficient manner. 
It extends Pydantic's `BaseModel` and adds several features to support pydantic-serdes's functionality.

Here is a high-level overview:

- **Instantiation**: An attempt to directly instantiate a `PydanticSerdesBaseModel` object will result in 
  `ModelInitializationError`. Additionally, direct instantiation of subclasses is discouraged. Instead, users should
   avail of the `create_from_loaded_data()` factory method that allows creating instances of a subclass
   from a dict or a list of dicts. Leveraging this method ensures that all instances are created in a controlled
   manner and properly recorded in the global data store.


- **Ordering and Hashing**: The class implements ordering and hashing, which allows instances to be stored in a 
  sorted set. This is useful for efficient retrieval and comparison of instances.


- **Sort Key**: To support the ordering and hashing, each instance has a unique identifier, or key, which is a tuple of 
  certain attribute values. This key is used to identify the instance in the global data store and also to sort the 
  instances.


- **Seamless Access to the Global Data Store**: The class has a reference to the global data store where all model 
  instances are stored. This allows for seamless addition of new instances of any of its subclasses to the 
  [GLOBAL_DATA_STORE](/docs/the_global_data_store.md). It also offers methods to retrieve a single instance, multiple 
  instances matching a criteria, or all instances of the model class through the following methods, respectively: 
  `get()`, `filter()` and `get_all()`.


- **Subclass Registry**: The class keeps track of all its subclasses. This is important for the discovering and 
  mapping of model classes to a 'directive' in the serialized data *(for more info on 'directive', keep reading).* 


- **Model-to-Directives Mapping**: In the context of pydantic-serdes, a 'directive' is a keyword in the 
  serialized data that holds a value (either a list or another set of key:value pairs) representing one or more 
  instances of models that should be created. `PydanticSerdesBaseModel` defines an optional `_directive` attribute.
  If a subclass chooses to include a value for this attribute, then the behavior will be to try and instantiate model 
  objects of that class for each element (be it one or several) nested under a keyword in the serialized data 
  matching the value of the `_directive` attribute. ***This is a powerful feature that allows for the automatic instantiation
  of model objects from serialized data***. Classes that don't define a value for the `_directive` 
  attribute can still be instantiated with serialized data, but it won't happen automatically, and the developer 
  would have to include custom logic to take care of that.


- **Duplication Handling**: Because each instance of a subclass of `PydanticSerdesBaseModel` will be stored in a 
  sorted set inside the GLOBAL_DATA_STORE, duplication is automatically never going to happen. The default behavior 
  when facing duplications will be the same as with Python's built-in set objects: silently ignore it. However, 
  setting `_error_on_duplicate` to True allows raising an error if an attempt is made to add a duplicate instance to
  the global data store.

**Users are encouraged to examine [PydanticSerdesBaseModel](/pydantic_serdes/models.py) code. It is fairly well documented and more
information can be found looking docstrings available.**

***

## [PydanticSerdesRenderableModel](/pydantic_serdes/models.py)
> ***Note**: The `PydanticSerdesRenderableModel` class is not meant to be directly instantiated. Instead, it should
> be subclassed to create model classes.*

The `PydanticSerdesRenderableModel` class extends the `PydanticSerdesBaseModel` and adds functionality for 
rendering instances into strings using Jinja2 templates. This can be useful for a number of automation or reporting 
tasks, where you need to generate text-based output based on the model data.

Here's a high-level overview:

- **Keeps all the good stuff**: `PydanticSerdesRenderableModel` inherits from `PydanticSerdesBaseModel`, so it 
  has all the features of that class, including instantiation, ordering and hashing, keying, model-to-directives 
  mapping, and interaction with the global data store. 


- **Rendering**: The class provides a method `.get_rendered_str()` to render the instance into a string using a 
  Jinja2 template. The template is determined based on the `_template_name` attribute, which can be set explicitly 
  in the child class or, will be set implicitly, using the class name (more info below). Additionally, by default, 
  template files are always expected to be in a `templates` folder that exists within the same working directory where
  the `python` command was run from. This can be changed with the environment variable `TEMPLATES`- see 
  [Configuration and Extensibility](/docs/configuration-and-extensibility.md)


- **Template Name**: The `_template_name` attribute is used to determine the template to use for rendering. If not 
  set in the child class, it defaults to the lowercase class name, separated by '_' on the capital letters, and  
  always excluding the word 'model' from it. For example:
  - *MyClass* -> my_class.j2
  - *OtherClassModel* -> other_class.j2
  - *ModelYetAnotherClass* -> yet_another_class.j2


- **Additional Rendering Variables**: The `.get_rendered_str()` method allows you to pass additional variables (not
  present among the model's instance attributes) that will be expected by the template. This can be useful if you
  need to include data that is not part of the model instance.

**Users are encouraged to examine [PydanticSerdesRenderableModel](/pydantic_serdes/models.py) code. It is fairly well documented and
more information can be found looking docstrings available.**