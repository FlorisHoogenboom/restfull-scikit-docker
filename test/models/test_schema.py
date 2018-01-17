from scikit_rest_wrapper.models import Schema
from scikit_rest_wrapper.exceptions.http import SchemaNotPresent
import unittest
from unittest.mock import MagicMock
import marshmallow
from types import ModuleType


class MockSchemaModule(ModuleType):
    class ModelSchema(marshmallow.Schema):
        pass


class MockLoader(object):
    def get_module(self, identifier):
        return MockSchemaModule


class MockInvalidSchemaModule(ModuleType):
    pass


class SchemaGetterTest(unittest.TestCase):
    def test_calls_loader(self):
        """Instantiating the schema should call the loader."""
        loader = MockLoader()
        loader.get_module = MagicMock(return_value=MockSchemaModule)

        model = Schema(loader)

        loader.get_module.assert_called_with('schema')

    def test_handles_nonspecified_schema(self):
        """It should handle a not specified model in the SchemaModule"""
        loader = MockLoader()
        loader.get_module = MagicMock(
            return_value=MockInvalidSchemaModule
        )

        with self.assertRaises(SchemaNotPresent):
            model = Schema(loader)

    def test_handles_module_not_found(self):
        """It should handle module not found exceptions"""
        loader = MockLoader()
        loader.get_module = MagicMock()
        loader.get_module.side_effect = ModuleNotFoundError(
            'Cannot find module schema'
        )

        with self.assertRaises(SchemaNotPresent):
            model = Schema(loader)
