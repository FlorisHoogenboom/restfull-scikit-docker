# restfull-scikit-docker
 
This project provides a basic Docker container that can be used as base for creating an restfull wrapper around scikit-learn models. 

## This project
This project is composed of two main parts:
- The source code for the RESTfull API
- A Dockerfile that wraps this code in an image that runs it using NGINX uWSGI.

The goal of this project is to provide a quick an simple way to deploy a Scikit-learn model to production

## Usage
To use this container two objects are needed (1) an fitted Scikit-learn __model__ instance (2) a __serializer__ (preferabbly based on [marshmallow](https://marshmallow.readthedocs.io/en/latest/), for else correct handling of errors is not guaranteed) that serializes a Python datastructure to something that can be used as input for your model.  The model should be stored as a pickled file in the `/app/objects` folder while the serializer should be stored as a Python script in the `/app/modules` folder. Pickling of the Scikit-learn model should be done using the `joblib` library included in `sklean.externals`.

### 1. The model and the schema
The model should be a fitted classifier that implements the Scikit-learn API (fit, transform etc.). This model should be stored as a pickeld file named _model_ in the folder `/app/objects`. Note that you need to use the version of the `joblib` library included wich Scikit-learn to correctly pickle a model.

The schema should be an subclass of `marshmallow.Schema` and should be named `ModelSchema`. You can use the `marshmallow.post_load` decorator to describe how data should be deserialized into a format that is accepted by your model. For example:

```{python}
from marshmallow import Schema, fields, post_load

class ModelSchema(Schema):
    param1 = fields.Str(required=True)
    param2 = fields.Int(required=True)

    @post_load
    def to_numpy_array(self, data):
        # your code here to transform the Dict data into 
        # e.g. a NumPy array
        return # Your desired datastructure.
``` 

### 2. Building the Docker image
In the folder you have saved your __schema.py__ and __model__ files, create a file named _Dockerfile_ with the following contents
```{Dockerfile}
FROM florishoogenboom/restfull-scikit-docker:latest

RUN {Install your dependencies here}

COPY ./model /app/objects/model
COPY ./schema.py /app/modules/schema.py
```
You can now build this image using `docker build -t myname/my-model . `. Note that you need to install the dependencies your model requires. This since unpickling requires the modules your model uses to be available.

### 3. Running the image
To run this image simply use `docker run -p 80:80 myname/my-model` this binds the model to port 80 locally. Of course you can use Docker swam to spin up multiple instances and make use of Dockers load balancing features.

## API Documentation

The API exposes the model by the following  endpoints
```
GET /json/
Returns: (JSON) A description of the model's schema.

Description: If the schema supplied implements a method description this endpoint returns the description given there. This is best used to describe the expected parameters.
```

```
GET /json/status
Returns: (JSON) The status of the model

Description: This endpoint is used to validate the status of the model. Of course, this should be tested at build however, due to Pythons dynamic nature not all issues may be spotted at this time.
```

```
POST /json/predict
Expects: A JSON object that can be parsed by the model's schema.
Returns: (JSON) The same object as provided, with the key 'target' added. This key contains the model's decision.

Description: Endpoint used to make a prediction using the model.
```

```
POST /json/predict/proba
Expects: A JSON object that can be parsed by the model's schema.
Returns: (JSON) The same object as provided, with the key 'target' added. This key contains an array with the predicted probabilities per class.

Description: Endpoint used to get probabilistic predictions.
```