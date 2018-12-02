import marshmallow
from ..exceptions.http import SchemaNotValid, SchemaNotPresent


class MarshmallowSchema(object):
    def __init__(self, loader):
        self.loader = loader
        self.schema = self._get()

    def _get(self):
        # TODO: handle errors here
        try:
            schema = self.loader\
                .get('schema')\
                .ModelSchema(strict=True)
        # TODO: Only catch if module not found is schema, otherwise raise again.
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

    def _has_descr(self):
        return hasattr(self.schema, 'describe')

    def describe(self):
        fields = self.schema.fields

        description = {}
        for field_name, field_def in fields.items():
            field_type = field_def.__class__.__name__
            field_descr = field_def.metadata.get(
                'description', 'No description available'
            )

            description[field_name] = '(%s) %s' % (field_type, field_descr)
        return description

    def load(self, data):
        return self.schema.load(data).data
