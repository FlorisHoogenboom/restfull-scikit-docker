from .bootstrap import App
from .routers import json

# Get the MonoState app
app = App().get_app()

# Register the routes for /json
app.register_blueprint(json.router, url_prefix='/json')