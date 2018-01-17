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
    schema_status = Schema.status(Loader())
    model_status = Model.status(Loader())

    if (schema_status !='ok' or model_status != 'ok'):
        status_code = 500
    else:
        status_code = 200

    return {
        'schema': schema_status,
        'model': model_status,
        'hostname': socket.gethostname()
    }, status_code


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
