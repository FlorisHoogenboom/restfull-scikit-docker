class BaseModel(object):
    def describe_requirements(self):
        raise NotImplementedError('This model cannot describe it\'s requirements.')

    def predict(self, data):
        raise NotImplementedError('This model has no predict capability.')

    def predict_proba(self, data):
        return NotImplementedError('This model has no predict_proba capability')


class LocalModel(BaseModel):
    def __init__(self, schema, processor):
        self.schema = schema
        self.processor = processor

    def describe_requirements(self):
        return self.schema.describe()

    def predict(self, data):
        return self.processor.predict(
            self.schema.load(data)
        )[0]

    def predict_proba(self, data):
        return self.processor.predict_proba(
            self.schema.load(data)
        )[0]
