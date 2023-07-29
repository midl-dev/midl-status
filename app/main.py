from flask import Flask

from app.config import Config
from app.extensions import register_extensions


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)

    return app
