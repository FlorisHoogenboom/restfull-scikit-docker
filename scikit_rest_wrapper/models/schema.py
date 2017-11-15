import marshmallow
from scikit_rest_wrapper.util import Loader
from scikit_rest_wrapper.exceptions.http import SchemaNotValid, SchemaNotPresent

class Schema(object):
    def __init__(self):
        pass

    def get(self):
        # TODO: handle errors here
        try:
            schema = Loader().get_module('schema').ModelSchema(
                strict=True
            )
        except ModuleNotFoundError:
            raise SchemaNotPresent()

        if not self.validate(schema):
            raise SchemaNotValid()

        return schema

    def validate(self, schema):
        return isinstance(
            schema,
            marshmallow.Schema
        )

    def status(self):
        try:
            self.get()
        except SchemaNotValid or SchemaNotPresent:
            return 'not ok'
        return 'ok'

    def has_descr(self, schema):
        return hasattr(schema, 'describe')

