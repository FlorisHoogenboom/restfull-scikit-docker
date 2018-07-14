from sklearn.externals import joblib
from scikit_rest_wrapper import config
from os.path import join
import sys
import importlib


class CachingLoader(object):
    loaded_objects = {}

    def get(self, identifier):
        if identifier not in self.loaded_objects.keys():
            self.__class__.loaded_objects[identifier] = self._get(identifier)

        return self.loaded_objects[identifier]


class ModuleLoader(CachingLoader):
    def _get(self, identifier):
        sys.path.append(config.OBJECTS_DIR)
        return importlib.import_module(identifier)


class SklearnJoblibLoader(CachingLoader):
    def _get(self, identifier):
        return joblib.load(join(config.OBJECTS_DIR, identifier))
