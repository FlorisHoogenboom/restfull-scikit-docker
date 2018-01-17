import marshmallow
from ..exceptions.http import SchemaNotValid, SchemaNotPresent


class Schema(object):
    def __init__(self, loader):
        self.loader = loader
        self.schema = self._get()

    def _get(self):
        # TODO: handle errors here
        try:
            schema = self.loader\
                .get_module('schema')\
                .ModelSchema(strict=True)
        except (ModuleNotFoundError, AttributeError):
            raise SchemaNotPresent()

        if not self._validate(schema):
            raise SchemaNotValid()

        return schema

    def _validate(self, schema):
        return isinstance(
            schema,
            marshmallow.Schema
        )

    def has_descr(self):
        return hasattr(self.schema, 'describe')

    def describe(self):
        if not self.has_descr():
            NotImplemented('Schema has no description implemented')
        return self.schema.describe()

    def load(self, data):
        return self.schema.load(data).data

    @staticmethod
    def status(loader):
        try:
            # Try to instantiate the schema
            Schema(loader)
        except (SchemaNotValid, SchemaNotPresent):
            return 'not ok'
        return 'ok'
