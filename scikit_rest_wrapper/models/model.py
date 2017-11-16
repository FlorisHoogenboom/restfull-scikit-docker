from ..util import Loader
from ..exceptions.http import (
    InvalidModel,
    ModelNotPresent,
    DependencyNotSatisfied
)
from sklearn.utils import validation
from sklearn.exceptions import NotFittedError


class Model(object):
    def __init__(self):
        pass

    def get(self):
        try:
            model = Loader().get_object('model')
        except FileNotFoundError:
            raise ModelNotPresent()
        except ModuleNotFoundError as e:
            raise DependencyNotSatisfied(
                'Dependency {0} cannot be found.'.format(e.name)
            )

        if not self.validate(model):
            raise InvalidModel()
        return model

    def _is_valid_model(self, model, attributes=[]):
        # TODO: Bad, practice, change default argument.
        try:
            # TODO: it is possible a model is not fitted even if this passes
            validation.check_is_fitted(model, attributes)
        except NotFittedError or TypeError:
            return False
        return True

    def validate(self, model):
        return self._is_valid_model(model)

    def status(self):
        try:
            model = self.get()
        except (
            ModelNotPresent,
            InvalidModel,
            ModuleNotFoundError
        ):
            return 'not ok'
        return 'ok'

    def has_predict_proba(self, model):
        return self._is_valid_model(model, ['predict_proba'])
