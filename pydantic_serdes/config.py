import importlib
import inspect
import os
from types import ModuleType
from typing import Dict, List, Type

from pydantic_serdes.exceptions import PydanticSerdesImportError

# Below, we define the default values for the environment variables that
# will be used to configure the package. If the user wants to override these
# values, they can do so by setting the environment variables with the same
# names as the ones defined below.

# Directory where templates are stored by default
TEMPLATES_DIR = "templates"

# The python dotted path to the class used for creating hashable dictionaries
HASHABLE_DICT_CLS = "pydantic_serdes.custom_collections.HashableDict"

# The python dotted path to the module the provides loader functions
LOADERS_MODULE = "pydantic_serdes.loaders"

# The python dotted path to the module that provides dumper functions
DUMPERS_MODULE = "pydantic_serdes.dumpers"

# The python dotted paths to all modules that contain subclasses of PydanticSerdesBaseModel
# as an environment variable, it's a comma-separated string of dotted paths.
# Example: "my_module1.models,my_module2.models"
MODELS_MODULES = "pydantic_serdes.models"


class PydanticSerdesConfig:
    """
    This class is used to hold the configuration of the package, which is
    determined by the environment variables.
    """

    # this attr is initialized as an empty dictionary and will be populated
    # whenever the self.directive_to_model_mapping property is called by
    # utils.create_all_models_from_dict function.
    _directive_to_model_mapping: Dict[str, Type] = {}

    @property
    def templates_dir(self) -> str:
        return os.environ.get("TEMPLATES_DIR", TEMPLATES_DIR)

    @property
    def hashable_dict_cls(self) -> str:
        return os.environ.get("HASHABLE_DICT_CLS", HASHABLE_DICT_CLS)

    @property
    def loaders_module_path(self) -> str:
        return os.environ.get("LOADERS_MODULE", LOADERS_MODULE)

    @property
    def loaders_module(self) -> ModuleType:
        try:
            loaders_module = importlib.import_module(self.loaders_module_path)
        except ImportError as err:
            raise PydanticSerdesImportError(err)

        return loaders_module

    @property
    def dumpers_module_path(self) -> str:
        return os.environ.get("DUMPERS_MODULE", DUMPERS_MODULE)

    @property
    def dumpers_module(self) -> ModuleType:
        try:
            dumpers_module = importlib.import_module(self.dumpers_module_path)
        except ImportError as err:
            raise PydanticSerdesImportError(err)

        return dumpers_module

    @property
    def supported_formats(self) -> List[str]:
        """
        For simplicity, we only take loaders as the basis to determine the supported formats.

        In this package, it's guaranteed to always exist a matching dumper for each loader.
        If you are using a custom loader module, you should also strive for the same.
        """
        supported_formats = [
            name.partition("_")[0]
            for name, obj in inspect.getmembers(self.loaders_module)
            if inspect.isfunction(obj) and "_loader" in name
        ]

        return supported_formats

    @property
    def models_modules(self) -> List[str]:
        return os.environ.get("MODELS_MODULES", MODELS_MODULES).split(",")

    @property
    def directive_to_model_mapping(self) -> Dict[str, type]:
        """
        Returns a dictionary with the directive names as keys and the dotted paths
        to the corresponding PydanticSerdesBaseModel subclass as values.

        Notice that this property returns self._directive_to_model_mapping, which will
        be set once and always return that same value.

        It's only if self._directive_to_model_mapping is empty that this method will
        try to populate it:
            - 1st: by importing all modules in self.models_modules; and
            - 2nd: by iterating over all subclasses of PydanticSerdesBaseModel that
              have the '_directive' field set.
        """
        if self._directive_to_model_mapping:
            return self._directive_to_model_mapping

        self._import_all_models_modules()

        # import here to avoid circular imports error
        from pydantic_serdes.models import PydanticSerdesBaseModel

        for cls in PydanticSerdesBaseModel.get_subclasses_with_directive():
            self._directive_to_model_mapping[cls._directive.get_default()] = cls

        return self._directive_to_model_mapping

    def _import_all_models_modules(self) -> None:
        """
        By importing all models returned by self.models_modules, this method ensures
        subclasses of PydanticSerdesBaseModel are registered for discovery.

        Notice this method should be treated as private. Refrain from calling it
        directly, as it's called automatically by self.directive_to_model_mapping.

        Raises:
            PydanticSerdesImportError: If any of the modules in self.models_modules
            cannot be imported.
        """
        for module in self.models_modules:
            try:
                importlib.import_module(module)
            except ImportError as err:
                raise PydanticSerdesImportError(err)


GLOBAL_CONFIGS = None


def get_config():
    global GLOBAL_CONFIGS

    if GLOBAL_CONFIGS is None:
        GLOBAL_CONFIGS = PydanticSerdesConfig()

    return GLOBAL_CONFIGS
