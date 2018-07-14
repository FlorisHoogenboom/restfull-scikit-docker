from .loaders import ModuleLoader, SklearnJoblibLoader
from .models import LocalModel
from .processors import SklearnProcessor
from .schemas import MarshmallowSchema


class ModelFactory(object):
    @staticmethod
    def build_sklearn_model():
        return LocalModel(
            MarshmallowSchema(ModuleLoader()),
            SklearnProcessor(SklearnJoblibLoader())
        )

    @staticmethod
    def build_model(model_type, **kwargs):
        if model_type == 'sklearn':
            return ModelFactory.build_sklearn_model()
