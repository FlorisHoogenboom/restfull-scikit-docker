from scikit_rest_wrapper.bootstrap import App
from scikit_rest_wrapper import config

if __name__ == "__main__":
    # Change directory specification for development
    config.OBJECTS_DIR = '../objects'

    # Start the app
    App().get_app().run(host='127.0.0.1', threaded=True, port=3000)
