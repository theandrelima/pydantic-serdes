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
from pathlib import Path
from typing import Any, Callable, Dict, Optional, Union

import toml
import yaml

from serial_bus.exceptions import SerialBusDumperError


def stream_dumper(dump_func: Callable[..., None]):
    def standard_dumper_func(
        data: Dict[Any, Any],
        file_path: Optional[Union[Path, str]] = None,
        *args,
        **kwargs
    ) -> str:
        """
        Decorator to dump data to a stream and optionally to a file.

        Args:
            data (Dict[Any, Any]): The data to be written to the serialized stream.
            file_path (Optional[Union[Path, str]], optional): The path to the
            file where the serialized data will be written. If provided, the data
            will be written to the specified file. If not provided, the data
            will only be written to the stream. Defaults to None.

        Returns:
            str: The string containing the written serialized data.

        Raises:
            SerialBusDumperError: If any exception occurs while dumping the data.
        """
        try:
            stream = io.StringIO()
            dump_func(data, stream, *args, **kwargs)

            if file_path is not None:
                with open(file_path, "w") as file:
                    file.write(stream.getvalue())

            return stream.getvalue()
        except Exception as e:
            raise SerialBusDumperError(str(e))

    return standard_dumper_func


@stream_dumper
def json_dumper(
    data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs
) -> str:
    """Writes data to a JSON stream and optionally to a file."""
    json.dump(data, stream, *args, **kwargs)


@stream_dumper
def yaml_dumper(
    data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs
) -> str:
    """Writes data to a YAML stream and optionally to a file."""
    yaml.dump(data, stream, *args, **kwargs)


@stream_dumper
def yml_dumper(
    data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs
) -> str:
    """Writes data to a YAML stream and optionally to a file."""
    yaml.dump(data, stream, *args, **kwargs)


@stream_dumper
def ini_dumper(
    data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs
) -> str:
    """Writes data to an INI stream and optionally to a file."""
    config = configparser.ConfigParser()
    config.read_dict(data)
    config.write(stream, *args, **kwargs)


@stream_dumper
def toml_dumper(
    data: Dict[Any, Any], stream: io.StringIO, *args, **kwargs
) -> str:
    """Writes data to a TOML stream and optionally to a file."""
    toml.dump(data, stream, *args, **kwargs)
