from scikit_rest_wrapper import App
from scikit_rest_wrapper.routers import json
from scikit_rest_wrapper.exceptions import configure_error_handlers

# Get the MonoState app
app = App().get_app()

# Configure default error handling
configure_error_handlers(app)

# Register the route for json
app.register_blueprint(json.router, url_prefix='/json')

# Start the application
app.run(host="0.0.0.0", port=80, threaded=True)
