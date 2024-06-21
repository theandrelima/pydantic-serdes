from pydantic import field_validator
from pydantic_serdes.custom_collections import OneToMany
from typing import Callable, Dict, Any, Optional, Union
from pathlib import Path
import io
from pydantic_serdes.exceptions import PydanticSerdesDumperError
from typing import TextIO


def onetomany_validators(cls):
    # Iterate over the class's annotations
    for field_name, field_type in cls.__annotations__.items():
        # Check if the field is a OneToMany field
        if getattr(field_type, '__origin__', None) is OneToMany:
            # If it is, add a validator for this field

            # Get the expected type of the elements
            expected_type = field_type.__args__[0]

            # Define the validator function
            def onetomany_validator(cls, v):
                if not all(isinstance(item, expected_type) for item in v):
                    raise TypeError(f'Each item in {field_name} must be a {expected_type.__name__} instance')
                return v

            # Add the validator to the class
            setattr(cls, f'validate_{field_name}', field_validator(field_name)(onetomany_validator))

    return cls


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
            PydanticSerdesDumperError: If any exception occurs while dumping the data.
        """
        try:
            stream = io.StringIO()
            dump_func(data, stream, *args, **kwargs)

            if file_path is not None:
                with open(file_path, "w") as file:
                    file.write(stream.getvalue())

            return stream.getvalue()
        except Exception as e:
            raise PydanticSerdesDumperError(str(e))

    return standard_dumper_func


def stream_loader(load_func: Callable[..., Dict]):
    """
    This decorator wraps a loader function to allow it to handle different types of input sources.

    Args:
        load_func (Callable[..., Dict]): The function that will be used to load and parse the data.
        This function should take a TextIO object as its first argument, which represents the stream of data to be
        loaded.
        It may also accept additional arguments, which will be passed through from the `standard_loader_func`.
        The function should return a dictionary representing the parsed data.
    """
    def standard_loader_func(source: Union[Path, str, TextIO], *args, **kwargs) -> dict:
        """
        This decorator wraps a loader function to allow it to handle different types of input sources.
        The input source can be a file path (as a string or Path object) or a TextIO object.
        If the source is a file path, the decorator opens the file and passes the file stream to the
        loader function. If the source is a TextIO object, it is passed directly to the loader function.

        Args:
            source (Union[Path, str, TextIO]): The source of the data to be loaded. This can be a file path (as a
            string or Path object), in which case the file will be opened and its contents passed to `load_func`.
            It can also be a TextIO object, in which case it will be passed directly to `load_func`.
            *args: Variable length argument list to be passed to `load_func`.
            **kwargs: Arbitrary keyword arguments to be passed to `load_func`.

        Returns:
            Callable: The decorated loader function.
        """

        if isinstance(source, (str, Path)):
            with open(source, "r") as stream:
                dictionary = load_func(stream, *args, **kwargs)
        else:
            dictionary = load_func(source, *args, **kwargs)

        return dictionary

    return standard_loader_func
