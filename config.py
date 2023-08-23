from os import environ, path

from celery.schedules import crontab
from dotenv import load_dotenv

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"), override=True)


class Config:
    """Flask configuration variables."""

    # General Config
    DEBUG = environ.get("FLASK_DEBUG")
    SECRET_KEY = environ.get("SECRET_KEY")

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")

    # Celery
    CELERY_BROKER_URL = environ.get("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = environ.get("CELERY_RESULT_BACKEND")
    CELERY_BEAT_SCHEDULE = {}

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATE_FOLDER = "templates"


class ProductionConfig(Config):
    ENV = "production"
    # MIDL public infrastructures
    MIDL_CLUSTER_INFO = [
        {
            "name": "MIDL.dev Toronto",
            "probe_url": environ.get("MIDL_TOR_URL"),
            "cluster_labels": environ.get("MIDL_TOR_CLUSTER_LABELS"),
            "injected_op_labels": environ.get("MIDL_TOR_INJECTED_OPS_LABELS"),
        },
        {
            "name": "MIDL.dev Amsterdam",
            "probe_url": environ.get("MIDL_AMS_URL"),
            "cluster_labels": environ.get("MIDL_AMS_CLUSTER_LABELS"),
            "injected_op_labels": environ.get("MIDL_AMS_INJECTED_OPS_LABELS"),
        },
    ]

    MIDL_LOKI_URL = environ.get("MIDL_LOKI_URL")

    CELERY_BEAT_SCHEDULE = {
        "check-cluster-status": {
            "task": "app.celery.check_cluster_status",
            "schedule": 30.0,
        },
        "fetch-cluster-request-counts": {
            "task": "app.celery.fetch_cluster_request_counts",
            "schedule": 60.0,
            "args": ("60s",),
        },
        "fetch-cluster-injected-ops": {
            "task": "app.celery.fetch_cluster_request_counts",
            "schedule": 60.0,
            "args": ("60s", "injected_ops"),
        },
        "cleanup-status-data": {
            "task": "app.celery.cleanup_status_data",
            "schedule": crontab(minute="0", hour="0"),
        },
    }


class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    # MIDL public infrastructures
    MIDL_CLUSTER_INFO = [
        {
            "name": "MIDL.dev Toronto",
            "probe_url": None,
            "cluster_labels": None,
            "injected_op_labels": None,
        },
        {
            "name": "MIDL.dev Amsterdam",
            "probe_url": None,
            "cluster_labels": None,
            "injected_op_labels": None,
        },
    ]

    MIDL_LOKI_URL = None

    CELERY_BEAT_SCHEDULE = {
        "check-cluster-status": {
            "task": "app.celery.check_cluster_status",
            "schedule": 30.0,
        },
        "fetch-cluster-request-counts": {
            "task": "app.celery.fetch_cluster_request_counts",
            "schedule": 60.0,
            "args": ("60s",),
        },
        "fetch-cluster-injected-ops": {
            "task": "app.celery.fetch_cluster_request_counts",
            "schedule": 60.0,
            "args": ("60s", "injected_ops"),
        },
        "cleanup-status-data": {
            "task": "app.celery.cleanup_status_data",
            "schedule": 60.0,
        },
    }


class TestingConfig(Config):
    ENV = "testing"
    DEBUG = True
    MIDL_CLUSTER_INFO = None
    MIDL_LOKI_URL = None
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{path.join(BASE_DIR, 'instance', 'app.db')}"
