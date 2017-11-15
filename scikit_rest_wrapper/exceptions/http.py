from werkzeug.exceptions import InternalServerError


class SchemaNotValid(InternalServerError):
    """"
    Exception used to indicate an invalid schema has been supplied.
    """
    description = ("The schema supplied is not valid"
                   "and cannot be used for modelling.")
    name = 'Schema Not Valid error'


class SchemaNotPresent(InternalServerError):
    """"
    Exception used to indicate no schema has been supplied.
    """
    description = ("No Schema has been supplied for serialization.")
    name = 'No schema has been supplied'


class InvalidModel(InternalServerError):
    """"
    Exception used to indicate an invalid model has been supplied
    """
    description = ("The model supplied is not valid.")
    name = 'An invalid model has been supplied'


class ModelNotPresent(InternalServerError):
    """"
    Exception used to indicate no model has been supplied
    """
    description = ("No model has been supplied.")
    name = 'No model has been supplied'

class DependencyNotSatisfied(InternalServerError):
    """
    Exception to indicate a dependency has not been satisfied while
    loading an object.
    """
    description = "Not all dependencies have been satisfied"