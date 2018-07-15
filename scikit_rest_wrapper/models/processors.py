from ..exceptions.http import (
    InvalidModel
)
from sklearn.utils import validation
from sklearn.exceptions import NotFittedError
import numpy as np


class BaseProcessor(object):
    def __init__(self, model):
        self.model = model

    @classmethod
    def from_loader(cls, loader, identifier='model'):
        model = loader.get(identifier)
        return cls(model)


class SklearnProcessor(BaseProcessor):
    @classmethod
    def from_loader(cls, loader, identifier='model'):
        model = super(SklearnProcessor, cls)\
            .from_loader(loader, identifier)

        if not cls._is_valid_model(model.model):
            raise InvalidModel('Model cannot be loaded')
        return model

    @staticmethod
    def _is_valid_model(model, attributes=None):
        if attributes is None:
            attributes = []

        try:
            # TODO: it is possible a model is not fitted even if this passes
            validation.check_is_fitted(
                model,
                attributes
            )
        except (NotFittedError, TypeError):
            return False
        return True

    def has_predict_proba(self):
        return self._is_valid_model(
            self.model,
            ['predict_proba', 'classes_']
        )

    def predict(self, data):
        return self.model \
            .predict(data) \
            .tolist()

    def predict_proba(self, data):
        if not self.has_predict_proba():
            raise NotImplementedError('Model cannot be used for probabilistic predictions')

        predictions = self.model.predict_proba(data).tolist()
        classes = self.model.classes_.tolist()

        # We convert the model result to include
        # the class names
        class_probabilities = []
        for prediction in predictions:
            class_probabilities.append(
                dict(zip(
                    classes,
                    prediction
                ))
            )

        return class_probabilities


class KerasClassifier(BaseProcessor):
    def predict(self, data):
        probas = self.model.predict(data)
        pred_indices = np.argmax(probas, axis=1)
        return pred_indices.tolist()

    def predict_proba(self, data):
        predictions = self.model.predict(data)
        # for now we use default labels 1,2,3,4
        classes = list(range(predictions.shape[-1]))

        # We convert the model result to include
        # the class names
        class_probabilities = []
        for prediction in predictions.tolist():
            class_probabilities.append(
                dict(zip(
                    classes,
                    prediction
                ))
            )

        return class_probabilities
