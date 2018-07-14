from sklearn.externals import joblib
from scikit_rest_wrapper import config
from os.path import join
import sys
import importlib


class BaseLoader(object):
    def get(self, identifier):
        return self._get(identifier)


class ModuleLoader(BaseLoader):
    def _get(self, identifier):
        sys.path.append(config.OBJECTS_DIR)
        return importlib.import_module(identifier)


class SklearnJoblibLoader(BaseLoader):
    def _get(self, identifier):
        return joblib.load(join(config.OBJECTS_DIR, identifier))
