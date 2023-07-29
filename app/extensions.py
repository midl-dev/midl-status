from celery import Celery
from flask_migrate import Migrate
from app.models import db

migrate = Migrate()
celery = Celery()


def register_extensions(app, worker=False):
    db.init_app(app)
    migrate.init_app(app, db)
    celery.config_from_object(app.config)
