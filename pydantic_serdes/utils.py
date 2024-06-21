import importlib
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Type, TypeVar, Union

from pydantic_serdes.config import get_config
from pydantic_serdes.exceptions import (PydanticSerdesImportError,
                                        PydanticSerdesTypeError,
                                        UnsupportedFileFormatError)

GLOBAL_CONFIGS = get_config()

# This module is where the 'HashableDict' will be used the most.
# Hence, we import it here and in pydantic_serdes.__init__.py we import
# it from here. Other modules, including client code, should always do
# 'from pydantic_serdes import HashableDict'.
_module, _, _cls = GLOBAL_CONFIGS.hashable_dict_cls.rpartition(".")
try:
    hashable_dict_module = importlib.import_module(_module)
    HashableDict = getattr(hashable_dict_module, _cls)
except AttributeError:
    raise PydanticSerdesImportError(
        f"Could not import class {_cls} from module {_module}"
    )

# Creating a generic type variable to be used in type hints for the HashableDict
# class. This is necessary because the class actually assigned to HashableDict is
# not known in advance, as it can be dynamically defined by the user.
HashableDictType = TypeVar("HashableDictType", bound=HashableDict)

if TYPE_CHECKING:
    from pydantic_serdes.models import PydanticSerdesBaseModel


def check_support_by_extension(file_path: Path) -> bool:
    """Checks if the file represented by `file_path` is of a
    supported format.

    Here we take a rather naive approach and only check the file
    extension.

    Args:
        file_path (Path): the path to the file to be checked.

    Raises:
        PydanticSerdesTypeError: If `file_path` does not represent a file.

    Returns:
        bool: True if the file is of a supported format, False otherwise.
    """
    if not file_path.is_file():
        raise PydanticSerdesTypeError(
            f"{file_path.absolute()} does not exist or is not a file."
        )
    return file_path.suffix.lstrip(".") in GLOBAL_CONFIGS.supported_formats


def load_file_to_dict(file_path: Union[str, Path]) -> dict:
    """Finds the appropriate loader for the file format and uses it to load the file.

    Args:
        file_path (str, Path): the path to the file to be loaded. If it's a
        string, it will be converted to a Path object.

    Raises:
        PydanticSerdesImportError: If the supplied module with loader
        functions can't be imported.
        UnsupportedFileFormatError: If the file format is not supported.

    Returns:
        dict: the loaded file as a dictionary.
    """
    if isinstance(file_path, str):
        file_path = Path(file_path)

    if not check_support_by_extension(file_path):
        raise UnsupportedFileFormatError(
            f"File extension {file_path.suffix.lstrip('.')} not supported. "
            f"Supported formats are {GLOBAL_CONFIGS.supported_formats}"
        )

    try:
        loader_function = getattr(
            GLOBAL_CONFIGS.loaders_module, f"{file_path.suffix.lstrip('.')}_loader"
        )
    except AttributeError:
        raise PydanticSerdesImportError(
            f"Could not find a loader function with name {file_path.suffix.lstrip('.')}_loader"
        )
    return loader_function(file_path)


def convert_src_file_to(
    src_file: Union[str, Path],
    dst_format: str,
    save_to_file: Optional[bool] = True,
    dst_file: Optional[Union[str, Path]] = None,
    *args,
    **kwargs,
) -> None:
    """
    Converts a serialized file to another format. Saves the content of
    converted data to a file and also returns the converted data as a string.

    Args:
        src_file (str, Path): the path to the file to be converted. Can be either
        a string or a Path object.
        dst_format (str): the format to which the file will be converted.
        save_to_file (Optional[bool]): If True, the converted data will be
        saved to a file. Defaults to True to keep compatibility with the original
        implementation of this method.
        dst_file (Optional[str, Path]): the path to the output file. If not
        provided, the output will be written to a file with the same name as the input
        file, but with the new extension. Defaults to None.

        Any additional arguments and keyword arguments will be passed to the dumper
        function.

    Raises:
        UnsupportedFileFormatError: If the src_file format is not supported.
        PydanticSerdesImportError: If a loader of dumper function can't be found
        for the dst_format respectively.
    """
    if isinstance(src_file, str):
        src_file = Path(src_file)

    if isinstance(dst_file, str):
        dst_file = Path(dst_file)

    loaded_dict = load_file_to_dict(src_file)

    try:
        dumper_function = getattr(GLOBAL_CONFIGS.dumpers_module, f"{dst_format}_dumper")
    except AttributeError:
        raise PydanticSerdesImportError(
            f"Could not find a dumper function with name {dst_format}_dumper"
        )

    if not save_to_file:
        dst_file = None
    else:
        dst_file = dst_file or src_file.with_suffix(f".{dst_format}")

    return dumper_function(loaded_dict, dst_file, *args, **kwargs)


def convert_flat_dict_to_hashabledict(dict_obj: dict) -> Type[HashableDictType]:
    """
    Converts a flat dictionary to a HashableDict.
    This function SHOULDN'T be used directly, but rather through
    `convert_dict_to_hashabledict` which will handle the
    conversion of nested dictionaries.

    Args:
        dict_obj (dict): the dictionary to be converted.

    Returns:
        Type[HashableDictType]: the converted dictionary as a HashableDict.
    """
    if not dict_obj:
        return HashableDict()

    if not isinstance(dict_obj, HashableDict):
        dict_obj = HashableDict(dict_obj)

    return dict_obj


def convert_dict_to_hashabledict(dict_obj: dict) -> Type[HashableDictType]:
    """Converts a nested dictionary to a HashableDict.

    Args:
        dict_obj (dict): the dictionary to be converted.

    Returns:
        Type[HashableDictType]: the converted dictionary as a HashableDict.
    """
    for k in dict_obj:
        if isinstance(dict_obj[k], dict):
            convert_dict_to_hashabledict(dict_obj[k])
            dict_obj[k] = convert_flat_dict_to_hashabledict(dict_obj[k])

    return convert_flat_dict_to_hashabledict(dict_obj)


def generate_from_dict(
    loaded_dict: dict,
) -> None:
    """
    Instantiate all pydantic-serdes models from a dictionary.

    Args:
        loaded_dict (dict): the dictionary to be used to create the models.

    Raises:
        DataTypeError: If `loaded_dict` is not a dict.

    """
    for key in loaded_dict:
        model_cls = GLOBAL_CONFIGS.directive_to_model_mapping.get(key)
        if model_cls:
            if isinstance(loaded_dict[key], list):
                for dict_element in loaded_dict[key]:
                    generate_from_dict(dict_element)

            model_cls.create_from_loaded_data(loaded_dict[key])


def generate_from_file(file_path: Union[str, Path]) -> None:
    """
    A very straightforward function to instantiate all models from a file.

    This will only work if there's no need for any kind of pre-processing of the
    data before creating the models.

    If there's a need for pre-processing, then a better approach would be to:
        1 - load the data as a dict by using `load_file_to_dict`
        2 - do the required processing of the loaded data
        3 - create the models from the processed data using `create_all_models_from_dict`

    Args:
        file_path (Union[str, Path]): The Path object or a str that can be converted to a
        Path object to the file containing serialized data to be loaded and parsed into a
        dictionary.
    """
    loaded_data = load_file_to_dict(file_path)
    generate_from_dict(loaded_dict=loaded_data)
