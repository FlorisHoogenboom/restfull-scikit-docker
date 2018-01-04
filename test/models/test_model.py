from scikit_rest_wrapper.models import Model
from sklearn.base import BaseEstimator
from scikit_rest_wrapper.exceptions.http import (
    ModelNotPresent,
    DependencyNotSatisfied
)

import unittest
from unittest.mock import MagicMock

class MockModel(BaseEstimator):
    """
    Mock of a Scikit-Learn model.
    """
    def fit(self, X, y):
        pass

    def predict(self, X, y):
        pass

class MockLoader(object):
    def get_object(self, identifier):
        return MockModel()

class MockLoaderFileNotFound(object):
    def get_object(self, identifier):
        raise FileNotFoundError()

class MockLoaderModuleNotFound(object):
    def get_object(self, identifier):
        raise ModuleNotFoundError(
            name='test_module'
        )

class ModelGetterTest(unittest.TestCase):
    """
    Testcase for the Model model (i.e. the model containing
    the scikit-learn model).
    """
    def test_calls_loader(self):
        """
        Instantiating a new model should call the loader.
        """
        loader = MockLoader()
        loader.get_object = MagicMock()

        model = Model(loader)

        loader.get_object.assert_called()
        loader.get_object.assert_called_with('model')

    def test_handles_file_not_found(self):
        """
        If the model is not found it should raise a ModelNotPresent exception.
        """
        loader = MockLoaderFileNotFound()
        with self.assertRaises(ModelNotPresent):
            model = Model(loader)

    def test_handles_module_not_found(self):
        """
        If the model cannot be deserialized it should raise a DependencyNotSatisfied error
        with the right dependency in the description.
        """
        loader = MockLoaderModuleNotFound()
        with self.assertRaisesRegex(
            DependencyNotSatisfied,
            'test_module'
        ):
            model = Model(loader)

    # TODO: Add test for model validation on load.

class ModelGetStatus(unittest.TestCase):
    def test_handles_correct_model(self):
        loader = MockLoader()

        self.assertEqual(
            Model.status(loader),
            'ok',
            'Model status should be \'ok\' for correctly loaded model.'
        )

    def test_handles_failing_model(self):
        # Model not found.
        loader = MockLoaderFileNotFound()
        self.assertEqual(
            Model.status(loader),
            'not ok',
            'Model status should be \'not ok\' for failing model.'
        )

        # Model cannot be deserialized
        loader = MockLoaderFileNotFound()
        self.assertEqual(
            Model.status(loader),
            'not ok',
            'Model status should be \'not ok\' for failing model.'
        )



class ModelPredictTest(unittest.TestCase):
    """
    Testcase for the models predict methods.
    """
    pass


