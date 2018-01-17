from scikit_rest_wrapper.models import Schema
import unittest
from unittest.mock import MagicMock
import marshmallow
from types import ModuleType

class MockLoader(object):
    pass

class MockSchemaModule(ModuleType):
    class ModelSchema(marshmallow.Schema):
        pass

class SchemaGetterTest(unittest.TestCase):
    def test_calls_loader(self):
        loader = MockLoader()
        loader.get_module = MagicMock(return_value=MockSchemaModule)

        model = Schema(loader)

        loader.get_module.assert_called_with('schema')
