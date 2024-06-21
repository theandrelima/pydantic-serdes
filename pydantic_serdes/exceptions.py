"""
Custom exceptions for pydantic-serdes are defined here.

The idea is to have subclasses of PydanticSerdesBaseException for each
possible error that can occur in the library. This way, the user can either
catch specific exceptions and handle them accordingly, or even use
PydanticSerdesBaseException as an umbrella to intercept any pydantic-serdes
specific error.
"""


class PydanticSerdesBaseException(Exception):
    """Parent class for all pydantic-serdes exceptions."""


class ModelInitializationError(PydanticSerdesBaseException):
    """Model instantiation is not possible."""


class PydanticSerdesTypeError(PydanticSerdesBaseException):
    """Data received is of the wrong type"""


class RenderableTemplateError(PydanticSerdesBaseException):
    """An error occurred while trying to render a RenderablePydanticSerdesModel"""


class ModelInstanceDoesNotExistError(PydanticSerdesBaseException):
    """The model does not exist in the datastore."""


class ModelInstanceAlreadyExistsError(PydanticSerdesBaseException):
    """Model already exists in the datastore."""


class MultipleModelInstancesReturnedError(PydanticSerdesBaseException):
    """More than one model instance found in the datastore matching search criteria, when only one should."""


class DataStoreDirectAssignmentError(PydanticSerdesBaseException):
    """Cannot directly assign to attribute 'records' of a ModelsGlobalStore object."""


class UnsupportedFileFormatError(PydanticSerdesBaseException):
    """Unsupported file format"""


class PydanticSerdesImportError(PydanticSerdesBaseException):
    """Error importing a module or class"""


class PydanticSerdesDumperError(PydanticSerdesBaseException):
    """Error dumping data"""
