# pydantic-serdes

pydantic-serdes is a Pydantic-based tool designed to act as a conduit between serialized data and Python objects. It 
not only facilitates the transformation of complex serialized data into Python objects, but also ensures stringent
data validation. Think of it as the wizard that transports your data from the realm of serialization into the world
of Python, and vice-versa, all the while maintaining the integrity and structure of your data. 

> *DISCLAMER*:
> Please note that this package was previously named `serial_bus` until version 0.2.0. To improve communication and 
> disambiguation, it has been renamed to `pydantic-serdes`. 


## Install

pip:

```bash
pip install pydantic-serdes
```

poetry:

```bash
poetry add pydantic-serdes
```

## Features

- **Pydantic Integration**: Converting serialized data into Python objects is the oldest trick in the book, but 
  pydantic-serdes elevates this process by directly converting the data into Pydantic models (and vice-versa), which 
  brings the added advantage of robust data validation. The models used in this process are defined by classes that 
  inherit from either the ***PydanticSerdesBaseModel*** or ***PydanticSerdesRenderableModel***. This not only 
  provides flexibility in setting up behaviors for your data, but also ensures data integrity through Pydantic's 
  validation mechanisms.


- **Built-in Support for Multiple Formats**: Currently, it supports loading serialized data from JSON, YAML, TOML 
  and INI. While future support for other formats is planned, if you need to cover additional formats, or even 
  provide your own parsing business logic, this can be easily achieved by extending pydantic-serdes basic 
  coverage with your own loader and/or dumper functions. Speaking of which...


- **Extensibility**: The code was thought to allow for ease of extensibility. For more information and examples, refer
to the documentation below.


<p align="center">
  <img src="https://github.com/theandrelima/pydantic-serdes/blob/main/docs/images/pydantic-serdes.png" alt="pydantic-serdes" width="300"/>
</p>


## Quick Start
  - [Usage examples](https://github.com/theandrelima/pydantic-serdes/blob/main/docs/getting_started.md#usage):
    - [Example 1: Instantiating models from serialized data](https://github.com/theandrelima/pydantic-serdes/blob/main/docs/getting_started.md#example-1-instantiating-models-from-serialized-data)
    - [Example 2: Data Relationship & Model Rendering](https://github.com/theandrelima/pydantic-serdes/blob/main/docs/getting_started.md#example-2-data-relationship--model-rendering)
    - [Example 3: Converting data between supported formats](https://github.com/theandrelima/pydantic-serdes/blob/main/docs/getting_started.md#example-3-converting-data-between-supported-formats)
  - [Configuration & Extensibility](https://github.com/theandrelima/pydantic-serdes/blob/main/docs/configuration-and-extensibility.md)
- [pydantic-serdes Base Models](https://github.com/theandrelima/pydantic-serdes/blob/main/docs/base_models.md)
- [The GLOBAL_DATA_STORE](https://github.com/theandrelima/pydantic-serdes/blob/main/docs/the_global_data_store.md)
- [Loaders](https://github.com/theandrelima/pydantic-serdes/blob/main/docs/loaders.md)
- [Dumpers](https://github.com/theandrelima/pydantic-serdes/blob/main/docs/dumpers.md)
- [Contributing](https://github.com/theandrelima/pydantic-serdes/blob/main/docs/contributing.md)
