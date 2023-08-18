from flask import Flask

from app.blueprints.home import home_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(home_bp)
