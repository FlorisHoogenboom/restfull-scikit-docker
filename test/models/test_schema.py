from scikit_rest_wrapper.models import Schema
from scikit_rest_wrapper.exceptions.http import SchemaNotPresent, SchemaNotValid
import unittest
from unittest.mock import MagicMock
import marshmallow
from types import ModuleType


class MockSchemaModule(ModuleType):
    class ModelSchema(marshmallow.Schema):
        pass

class MockSchemaModuleWithDescription(ModuleType):
    class ModelSchema(marshmallow.Schema):
        def describe(self):
            return "a description"


class MockSchemaModuleInvalidType(ModuleType):
    class ModelSchema(object):
        def __init__(self, *args, **kwargs):
            pass


class MockInvalidSchemaModule(ModuleType):
    pass


class MockLoader(object):
    def __init__(self, schema_module):
        self.schema_module = schema_module

    def get_module(self, identifier):
        return self.schema_module


class SchemaGetterTest(unittest.TestCase):
    def test_calls_loader(self):
        """Instantiating the schema should call the loader."""
        loader = MockLoader(MockSchemaModule)
        loader.get_module = MagicMock(return_value=MockSchemaModule)

        schema = Schema(loader)

        loader.get_module.assert_called_with('schema')

    def test_handles_nonspecified_schema(self):
        """It should handle a not specified model in the SchemaModule"""
        loader = MockLoader(MockInvalidSchemaModule)

        with self.assertRaises(SchemaNotPresent):
            schema = Schema(loader)

    def test_handles_module_not_found(self):
        """It should handle module not found exceptions"""
        loader = MockLoader(None)
        loader.get_module = MagicMock()
        loader.get_module.side_effect = ModuleNotFoundError(
            'Cannot find module schema'
        )

        with self.assertRaises(SchemaNotPresent):
            schema = Schema(loader)

    def test_handles_invalid_schema_type(self):
        """It should raise an error when not a marshmallow schema is passed."""
        loader = MockLoader(None)
        loader.get_module = MagicMock(return_value=MockSchemaModuleInvalidType)

        with self.assertRaises(SchemaNotValid):
            schema = Schema(loader)


class SchemaDescribeTest(unittest.TestCase):
    def test_handles_missing_description(self):
        """It should handle a schema without description"""
        schema = Schema(
            MockLoader(MockSchemaModule)
        )

        with self.assertRaises(NotImplementedError):
            schema.describe()

    def test_handles_existing_description(self):
        schema = Schema(
            MockLoader(MockSchemaModuleWithDescription)
        )

        self.assertEqual(
            schema.describe(),
            "a description"
        )
