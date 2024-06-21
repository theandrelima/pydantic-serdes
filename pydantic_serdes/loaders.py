"""
This module contains functions for loading data from various file formats.
It includes functions for loading data from JSON, YAML, TOML and INI files. 
Each function takes an input that holds a reference to the serialized data,
then it parses the data, and returns a Python dictionary. By default,
pydantic-serdes finds which loader to use automatically based on the file
extension through utils.load_file_to_dict() function. If the file format is
not supported, an UnsupportedFileFormatError is raised.

If your project uses file formats other than the ones supported here, you can
add support for them by having your own python loader module and creating an
environment variable `LOADERS_MODULE` that points to its dotted path.
The module should contain functions with the following naming convention:
`{format}_loader` where `format` is the file extension.

Each function should take an argument that brings the serialized data,
and return a dictionary. For example, if you have a custom file format with
the extension `.xyz`, you should create a function called `xyz_loader` in your
custom loaders module that could take a Path object, a str representing the
file system path to the file, or even a string containing the serialized
data itself. After parsing that data, your function must return a dictionary.
"""

import configparser
import json
from pathlib import Path
from typing import TextIO, Union

import toml
import yaml

from pydantic_serdes.decorators import stream_loader


@stream_loader
def json_loader(source: Union[Path, str, TextIO], *args, **kwargs) -> dict:
    """Parses a json text stream and returns a dictionary with its contents."""
    return json.load(source, *args, **kwargs)


@stream_loader
def yaml_loader(source: Union[Path, str, TextIO], *args, **kwargs) -> dict:
    """Parses a yaml text stream and returns a dictionary with its contents."""

    # yaml.load doesn't take any *args, **kwargs
    return yaml.load(source, Loader=yaml.FullLoader)


@stream_loader
def toml_loader(source: Union[Path, str, TextIO], *args, **kwargs) -> dict:
    """Parses a toml text stream and returns a dictionary with its contents."""
    return toml.load(source, *args, **kwargs)


@stream_loader
def ini_loader(source: Union[Path, str, TextIO], *args, **kwargs) -> dict:
    """Parses an ini text stream and returns a dictionary with its contents."""
    config = configparser.ConfigParser()
    config.read_file(source, *args, **kwargs)
    dictionary = {s: dict(config.items(s)) for s in config.sections()}
    return dictionary


def yml_loader(source: Union[Path, str, TextIO], *args, **kwargs) -> dict:
    """This is just to support .yml files. Essentially, it's the same as yaml_loader"""
    return yaml_loader(source, *args, **kwargs)
