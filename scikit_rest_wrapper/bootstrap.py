from flask import (
    Flask as FlaskOrig,
    request
)
from flask_json import FlaskJSON


# This is a backport from Flask 1.0, and it is used to help handle
# exceptions. This code should be removed once Flask 1.0 is out.
class Flask(FlaskOrig):
    def _find_error_handler(self, e):
        """
        Method that finds the handler for a specific exception class.
        :param e: Exception class that should be found
        :return: Exception handler for the exception class specified
        """
        exc_class, code = self._get_exc_class_and_code(type(e))
        for name, c in ((request.blueprint, code), (None, code),
                        (request.blueprint, None), (None, None)):
            handler_map = self.error_handler_spec.setdefault(name, {}).get(c)
            if not handler_map:
                continue
            for cls in exc_class.__mro__:
                handler = handler_map.get(cls)
                if handler is not None:
                    return handler


class App(object):
    app = None
    json = None

    def __init__(self):
        """
        Monostate class to serve as a factory for the Flask application.
        """
        pass

    def _register_app(self):
        """
        Method that registers a new app an corresonding json object
        :return: None
        """
        self.__class__.app = \
            Flask(__name__)
        self._register_json()

    def _register_json(self):
        """
        Method that registers a new json object, and a new app if the latter
        does not exist.
        :return: None
        """
        app = self.get_app()
        self.__class__.json = FlaskJSON(app)

    def get_app(self):
        """
        Method that creates or retrieves an app.
        :return: A unique instance of a Flask application
        """
        if self.app is None:
            self._register_app()
        return self.app

    def get_json(self):
        """
        Method that creates or retrieves a FlaskJSON instance
        :return: A unique instance of FlaskJSON
        """
        if self.json is None:
            self._register_json()
        return self.json