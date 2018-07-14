from werkzeug.exceptions import NotImplemented


class MainController(object):
    def __init__(self, model):
        self.model = model

    def index(self):
        """
        Controller that fetches the description of the model schema. Raises NotImplemented exception if
        it does not exist.
        :return: result of the describe method of the model schema if it exists.
        """

        return self.model.describe_requirements()

    def predict(self, data):
        """
        :param data: A datastructure serializable by the model schema
        :return: A copy of data with added the predicted class
        """
        prediction = self.model.predict(data)
        return {
            'target': prediction
        }

    def predict_proba(self, data):
        """

        :param data: An datastructure serializable by the model schema
        :return: A copy of data with added the prediction
        """
        try:
            prediction = self.model.predict_proba(data)
        except NotImplementedError:
            raise NotImplemented('This model cannot output probabilities.')

        return {
            'target': prediction
        }
