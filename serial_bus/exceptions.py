"""
Custom exceptions for SerialBus are defined here.

The idea is to have subclasses of SerialBusBaseException for each
possible error that can occur in the library. This way, the user can either
catch specific exceptions and handle them accordingly, or even use
SerialBusBaseException as an umbrella to intercept any SerialBus
specific error.
"""


class SerialBusBaseException(Exception):
    """Parent class for all SerialBus exceptions."""


class ModelInitializationError(SerialBusBaseException):
    """Model instantiation is not possible."""


class SerialBusTypeError(SerialBusBaseException):
    """Data received is of the wrong type"""


class RenderableTemplateError(SerialBusBaseException):
    """An error occurred while trying to render a RenderableSerialBusModel"""


class ModelDoesNotExistError(SerialBusBaseException):
    """The model does not exist in the datastore."""


class ModelAlreadyExistsError(SerialBusBaseException):
    """Model already exists in the datastore."""


class DataStoreDirectAssignmentError(SerialBusBaseException):
    """Cannot directly assign to attribute 'records' of a ModelsGlobalStore object."""


class UnsupportedFileFormatError(SerialBusBaseException):
    """Unsupported file format"""


class SerialBusImportError(SerialBusBaseException):
    """Error importing a module or class"""


class SerialBusDumperError(SerialBusBaseException):
    """Error dumping data"""
