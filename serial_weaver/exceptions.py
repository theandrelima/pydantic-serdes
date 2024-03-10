"""
Custom exceptions for serial_weaver are defined here.

The idea is to have subclasses of SerialWeaverBaseException for each
possible error that can occur in the library. This way, the user can either
catch specific exceptions and handle them accordingly, or even use
SerialWeaverBaseException as an umbrella to intercept any serial_weaver
specific error.
"""


class SerialWeaverBaseException(Exception):
    """Parent class for all serial_weaver exceptions."""


class ModelInitializationError(SerialWeaverBaseException):
    """Model instantiation is not possible."""


class SerialWeaverTypeError(SerialWeaverBaseException):
    """Data received is of the wrong type"""


class RenderableTemplateError(SerialWeaverBaseException):
    """An error occurred while trying to render a RenderableSerialWeaverModel"""


class ModelDoesNotExistError(SerialWeaverBaseException):
    """The model does not exist in the datastore."""


class ModelAlreadyExistsError(SerialWeaverBaseException):
    """Model already exists in the datastore."""


class DataStoreDirectAssignmentError(SerialWeaverBaseException):
    """Cannot directly assign to attribute 'records' of a ModelsGlobalStore object."""


class UnsupportedFileFormatError(SerialWeaverBaseException):
    """Unsupported file format"""


class SerialWeaverImportError(SerialWeaverBaseException):
    """Error importing a module or class"""


class SerialWeaverDumperError(SerialWeaverBaseException):
    """Error dumping data"""
