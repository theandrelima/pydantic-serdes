# SerialBus

SerialBus is a Pydantic-based tool designed to act as a conduit between serialized data and Python objects. It 
not only facilitates the transformation of complex serialized data into Python objects, but also ensures stringent
data validation. Think of it as the coach that transports your data from the realm of serialization into the world
of Python, and vice-versa, all the while maintaining the integrity and structure of your data.

## Install

pip:

```bash
pip install serial_bus
```

poetry:

```bash
poetry add serial_bus
```

## Features

- **Pydantic Integration**: Converting serialized data into Python objects is the oldest trick in the book, but 
  SerialBus elevates this process by directly converting the data into Pydantic models, which brings 
  the added advantage of robust data validation. The models used in this process are defined by classes that inherit 
  from either the ***SerialBusBaseModel*** or ***SerialBusRenderableModel***. This not only provides 
  flexibility in setting up behaviors for your data, but also ensures data integrity through Pydantic's validation 
  mechanisms.


- **Built-in Support for Multiple Formats**: Currently, it supports loading serialized data from JSON, YAML, TOML 
  and INI. While future support for other formats is planned, if you need to cover additional formats, or even 
  provide your own parsing business logic, this can be easily achieved by extending SerialBusbasic 
  coverage with your own loader and/or dumper functions. Speaking of which...


- **Extensibility**: The code was thought to allow for ease of extensibility. For more information and examples, refer
to the documentation below.


<p align="center">
  <img src="/docs/images/serial_bus.png" alt="SerialBus" width="300"/>
</p>


## Quick Start
  - [Usage examples](/docs/getting_started.md#usage):
    - [Example 1: Instantiating models from serialized data](/docs/getting_started.md#example-1-instantiating-models-from-serialized-data)
    - [Example 2: Data Relationship & Model Rendering](/docs/getting_started.md#example-2-data-relationship--model-rendering)
    - [Example 3: Converting data between supported formats](/docs/getting_started.md#example-3-converting-data-between-supported-formats)
  - [Configuration & Extensibility](docs/configuration-and-extensibility.md)
- [SerialBus Base Models](/docs/base_models.md)
- [The GLOBAL_DATA_STORE](/docs/the_global_data_store.md)
- [Loaders](/docs/loaders.md)
- [Dumpers](/docs/dumpers.md)
- [Contributing](#contributing)
