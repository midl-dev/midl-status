from celery import Celery
from flask import Flask
from flask_migrate import Migrate

from app.models import db

migrate = Migrate()
celery = Celery()


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    celery.config_from_object(app.config)
