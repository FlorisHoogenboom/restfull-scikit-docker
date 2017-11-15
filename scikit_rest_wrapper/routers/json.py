from flask import Blueprint
from flask_json import as_json
from flask import request
from werkzeug.exceptions import BadRequest
import controllers

# Initialize this router
router = Blueprint('json', __name__)


def validate_and_parse_json(request):
    """
    Function that validates for specific HTTP methods if the request
    passed is valid, and raises if it is not.
    :param request: A Flask request object
    :return: None
    """
    if (
        request.method in ['POST', 'PUT', 'UPDATE'] and not
        request.is_json
    ):
        raise BadRequest('Request should be valid JSON')
    return request.get_json()


@router.before_request
def before_request():
    """
    Method that validates request to the JSON router.
    :return: None
    """
    request.parsed = validate_and_parse_json(request)


# Routes for this router
@router.route('/')
@as_json
def index():
    return controllers.index()


@router.route('/status')
@as_json
def status():
    return controllers.status()


@router.route('/predict', methods=['POST'])
@as_json
def predict():
    return controllers.predict(request.parsed)


@router.route('/predict/proba', methods=['POST'])
@as_json
def predict_proba():
    return controllers.predict_proba(request.parsed)