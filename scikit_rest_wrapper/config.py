import os

OBJECTS_DIR = './objects'
MODULES_DIR = './modules'
DEBUG = os.environ.get('DEBUG') == "1"

CORS = os.getenv('CORS', '*')
CORS_HEADERS = os.getenv('CORS_HEADERS', 'Content-Type, Authorization')