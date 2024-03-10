# Serial Weaver

A pydantic based tool that standardizes the representation of serialized data as python objects not only capable of 
exhibiting complex business logic behaviors, but also ensuring stringent data validation.

## Install

pip:

```bash
pip install serial_weaver
```

poetry:

```bash
poetry add serial_weaver
```

## Features

- **Pydantic Integration**: Converting serialized data into Python objects is the oldest trick in the book, but 
  Serial Weaver elevates this process by directly converting the data into Pydantic models, which brings 
  the added advantage of robust data validation. The models used in this process are defined by classes that inherit 
  from either the ***SerialWeaverBaseModel*** or ***SerialWeaverRenderableModel***. This not only provides 
  flexibility in setting up behaviors for your data, but also ensures data integrity through Pydantic's validation 
  mechanisms.

- **Built-in Support for Multiple Formats**: Currently, it supports loading serialized data from JSON, YAML, TOML 
  and INI. While future support for other formats is planned, if you need to cover additional formats, or even 
  provide your own parsing business logic, this can be easily achieved by extending Serial Weaver basic 
  coverage with your own loader and/or dumper functions. Speaking of which...

- **Extensibility**: The code was thought to allow for ease of extensibility. For example, if you wish to add your own 
  loader function(s) you only have to define them in a python module and have an environment var named `LOADERS_MODULE` 
  containing the python dotted path to your module. The same idea applies to dumper functions: a custom module with 
  them defined and a `DUMPERS_MODULE` env var. For more information and examples, refer to the [Configuration & 
  Extensibility](docs/configuration-and-extensibility.md) section.  

## Quick Start
  - [Usage examples](/docs/getting_started.md#usage):
    - [Example 1: Instantiating models from serialized data](/docs/getting_started.md#example-1-instantiating-models-from-serialized-data)
    - [Example 2: Data Relationship & Model Rendering](/docs/getting_started.md#example-2-data-relationship--model-rendering)
    - [Example 3: Converting data between supported formats](/docs/getting_started.md#example-3-converting-data-between-supported-formats)
  - [Configuration & Extensibility](docs/configuration-and-extensibility.md)
- [SerialWeaver Base Models](/docs/base_models.md)
- [The GLOBAL_DATA_STORE](/docs/the_global_data_store.md)
- [Loaders](/docs/loaders.md)
- [Dumpers](/docs/dumpers.md)
- [Contributing](#contributing)

