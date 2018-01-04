from ..exceptions.http import (
    InvalidModel,
    ModelNotPresent,
    DependencyNotSatisfied
)
from sklearn.utils import validation
from sklearn.exceptions import NotFittedError


class Model(object):
    def __init__(self, loader):
        self.loader = loader
        self.model = self._get()

    def _get(self):
        try:
            model = self.loader.get_object('model')
        except FileNotFoundError:
            raise ModelNotPresent()
        except ModuleNotFoundError as e:
            raise DependencyNotSatisfied(
                'Dependency {0} cannot be found.'.format(e.name)
            )

        if not self._validate(model):
            raise InvalidModel()
        return model

    def _is_valid_model(self, model, attributes=None):
        # Assign default value for attributes
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

    def _validate(self, model):
        return self._is_valid_model(model)

    def has_predict_proba(self):
        return self._is_valid_model(
            self.model,
            ['predict_proba', 'classes_']
        )

    def predict(self, data):
        return self.model\
            .predict(data)\
            .tolist()

    def predict_proba(self, data):
        if not self.has_predict_proba():
            # TODO: Check how this is handled upstream?
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

    @staticmethod
    def status(loader):
        try:
            model = Model(loader)
        except (
            ModelNotPresent,
            InvalidModel,
            DependencyNotSatisfied
        ):
            return 'not ok'
        return 'ok'