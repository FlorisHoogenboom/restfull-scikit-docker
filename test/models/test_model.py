from scikit_rest_wrapper.models import Model
import numpy as np
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

    def predict(self, X):
        pass


class MockLoader(object):
    model = MockModel()

    def get_object(self, identifier):
        return self.model


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
    def test_predict(self):
        """
        Test predict calls the predict method of the model
        """
        loader = MockLoader()
        model = Model(loader)
        mock_model = loader.model

        # Mock the actual models predict function to test if it
        # is called correctly
        actual_result = np.array([1,2,3])
        mock_model.predict = MagicMock(
            return_value = actual_result
        )

        # Call the Model model predict function with some data
        data = np.array([
            [1,2],
            [4,6]
        ])
        result = model.predict(data)

        mock_model.predict.assert_called_once_with(data)

        self.assertListEqual(
            list(actual_result),
            result,
            'The predict method should return a list with predictions.'
        )


class ModelPredictProbaTest(unittest.TestCase):
    """
    Test the behavior for models having predict proba
    """
    def setUp(self):

        proba_model = MockModel()
        proba_model.predict_proba = MagicMock(
            return_value=np.array([
                [0,1],
                [0.223,0.777]
            ])
        )

        proba_model.classes_ = np.array(['class_1', 'class_2'])

        loader = MockLoader()
        loader.model = proba_model

        self.actual_model = proba_model
        self.model = Model(loader)

    def test_has_predict_proba(self):
        """
        Test if has_predict_proba correctly specifies if model has predict probability method
        """
        self.assertTrue(
            self.model.has_predict_proba(),
            "has_predict_proba should return true."
        )

        self.assertFalse(
            Model(MockLoader()).has_predict_proba(),
            "has_predict_proba should be false for model without predict_proba."
        )

    def test_raises_not_implemented(self):
        """
        Test if NotImplementedExcption is raised when called on model without predict_proba
        """
        model_without_predict_proba = Model(MockLoader())

        with self.assertRaises(NotImplementedError):
            model_without_predict_proba.predict_proba(
                np.array([[1,2,3]])
            )

    def test_predict_proba(self):
        data = np.array([
            [1,2],
            [3,4]
        ])
        result = self.model.predict_proba(data)

        self.actual_model.predict_proba.assert_called_once_with(data)

        self.assertEqual(result[0]['class_1'], 0)
        self.assertEqual(result[0]['class_2'], 1)

