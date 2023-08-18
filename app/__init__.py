import os

from flask import Flask

from app.blueprints import register_blueprints
from app.extensions import register_extensions


def create_app() -> Flask:
    # Create the Flask application
    app = Flask(__name__)

    # Configure the Flask application
    config_type = os.getenv("CONFIG_TYPE", default="config.DevelopmentConfig")
    app.config.from_object(config_type)

    register_extensions(app)
    register_blueprints(app)

    return app
