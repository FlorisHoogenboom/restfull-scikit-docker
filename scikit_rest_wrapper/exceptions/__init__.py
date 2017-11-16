from ..config import DEBUG
from flask_json import as_json
from werkzeug.exceptions import HTTPException
from marshmallow import ValidationError


def configure_error_handlers(app):
    @app.errorhandler(ValidationError)
    @as_json
    def handle_validation_error(error):
        """
        Error handler specific for validation errors.
        :param error: ValidationError instance
        :return: Dict containing the message and the validation
            errors, statuscode
        """
        return {
            'message': 'Validation errors occurred',
            'validation_errors': error.messages
        }, 400


    @app.errorhandler(Exception)
    @as_json
    def handle_error(error):
        """
        Error handler that serializes all error objects to a dict.
        :param error:
        :return: A dict containing the most important error parameters
        """
        if isinstance(error, HTTPException):
            return {
                       'summary': error.name,
                       'message': error.description
                   }, error.code
        elif not DEBUG:
            return {
                'summary': "An internal error occurred"
            }, 500
        else:
            raise error
