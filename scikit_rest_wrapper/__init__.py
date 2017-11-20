from .bootstrap import App
from .routers import json
from .exceptions import configure_error_handlers

# Get the MonoState app
app = App().get_app()

# Configure default error handling
configure_error_handlers(app)

# Register the routes for /json
app.register_blueprint(json.router, url_prefix='/json')