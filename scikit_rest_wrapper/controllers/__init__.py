from ..models import Model, Schema
from ..util import Loader
import socket


def index():
    """
    Controller that fetches the description of the model schema. Raises NotImplemented exception if
    it does not exist.
    :return: result of the describe method of the model schema if it exists.
    """
    model_schema = Schema(Loader())

    return model_schema.describe()


def status():
    """
    Controller that returns some statistics about the app.
    :return: A dict having keys 'model', 'schema', 'hostname'
    """

    return {
        'schema': Schema.status(
            Loader()
        ),
        'model': Model.status(
            Loader()
        ),
        'hostname': socket.gethostname()
    }


def predict(data):
    """
    :param data: An datastructure serializable by the model schema
    :return: A copy of data with added the predicted class
    """
    model_schema = Schema(Loader())
    model = Model(Loader())

    X = model_schema.load(data)
    y = model.predict(X)

    data['target'] = y[0]

    return data


def predict_proba(data):
    """

    :param data: An datastructure serializable by the model schema
    :return: A copy of data with added the prediction
    """
    model_schema = Schema(Loader())
    model = Model(Loader())

    X = model_schema.load(data)
    y = model.predict_proba(X)

    data['target'] = y[0]

    return data
