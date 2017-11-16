from sklearn.externals import joblib
from . import config
from os.path import join
import sys
import importlib


class Loader(object):
    objects = {}
    modules = {}

    def __init__(self):
        """
        A Loader class that facilitated load once, read from
        memory afterwards behavior.
        """
        pass

    def get_object(self, identifier):
        """
        Method that retrieves an object from a file using joblib.load
        :param identifier: a string specifying the object to be loaded from the config.data dir.
        :return: The unpickled object.
        """
        if identifier not in self.objects.keys():
            self.__class__.objects[identifier] = joblib.load(
                join(config.OBJECTS_DIR, identifier)
            )
        return self.objects[identifier]

    def get_module(self, identifier):
        """
        Method that loads a module based on its identifier.
        :param identifier: Name of the module to be loaded
        :return: The desired module
        """
        sys.path.append(config.MODULES_DIR)
        if identifier not in self.modules.keys():
            self.__class__.modules[identifier] = importlib.import_module(identifier)

        return self.modules[identifier]

