from .loaders import ModuleLoader, SklearnJoblibLoader, KerasLoader
from .models import LocalModel
from .processors import SklearnProcessor, KerasClassifier
from .schemas import MarshmallowSchema


class ModelFactory(object):
    @staticmethod
    def build_sklearn_model():
        return LocalModel(
            MarshmallowSchema(ModuleLoader()),
            SklearnProcessor.from_loader(SklearnJoblibLoader())
        )

    @staticmethod
    def build_keras_model():
        return LocalModel(
            MarshmallowSchema(ModuleLoader()),
            KerasClassifier.from_loader(KerasLoader())
        )

    @staticmethod
    def build_model(model_type, **kwargs):
        if model_type == 'sklearn':
            return ModelFactory.build_sklearn_model()
        elif model_type == 'keras':
            return ModelFactory.build_keras_model()
