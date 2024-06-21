"""
This module contains functions for creating serialized data in all supported formats.

Each function takes a Python dictionary, serializes the data, and writes it 
to a TextStream object. Optionally, a file can be created with the contents
of that TextStream if the dumper function is provided with a file path, which
can be either a Path or a str object.

If your project uses file formats other than the ones supported here, you can
add support for them by having your own python dumpers.py module and creating an
environment variable `DUMPERS_MODULE` that points to its dotted path.

Contrary to the loaders module, there's no mechanism for automatically detecting
which dumper function to use. A caller must be explicit about the dumper function
for the desired serialization format.
"""

import configparser
import io
import json
from typing import Any, Dict

import toml
import yaml

from pydantic_serdes.decorators import stream_dumper


@stream_dumper
def json_dumper(data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs) -> str:
    """Writes data to a JSON stream and optionally to a file."""
    json.dump(data, stream, *args, **kwargs)


@stream_dumper
def yaml_dumper(data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs) -> str:
    """Writes data to a YAML stream and optionally to a file."""
    yaml.dump(data, stream, *args, **kwargs)


@stream_dumper
def yml_dumper(data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs) -> str:
    """Writes data to a YAML stream and optionally to a file."""
    yaml.dump(data, stream, *args, **kwargs)


@stream_dumper
def ini_dumper(data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs) -> str:
    """Writes data to an INI stream and optionally to a file."""
    config = configparser.ConfigParser()
    config.read_dict(data)
    config.write(stream, *args, **kwargs)


@stream_dumper
def toml_dumper(data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs) -> str:
    """Writes data to a TOML stream and optionally to a file."""
    toml.dump(data, stream, *args, **kwargs)
