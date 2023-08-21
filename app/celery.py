import random
from datetime import datetime, timedelta

import requests
from celery import Celery

# from celery.schedules import crontab
from celery.utils.log import get_task_logger
from flask import Flask
from loki_api_client.loki_connect import LokiConnect

from app import create_app
from app.models import ClusterStatus, RequestCount, db

logger = get_task_logger(__name__)


def create_celery(app: Flask) -> Celery:
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
        beat_schedule=app.config["CELERY_BEAT_SCHEDULE"],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):  # type: ignore
        abstract = True

        def __call__(self, *args, **kwargs):  # type: ignore
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask  # type: ignore
    return celery


flask_app = create_app()
celery = create_celery(flask_app)


@celery.task
def check_cluster_status() -> None:
    for cluster in flask_app.config["MIDL_CLUSTER_INFO"]:
        cluster_name, cluster_probe_url = cluster["name"], cluster["probe_url"]
        cluster_status = ClusterStatus(cluster=cluster_name, time=datetime.now())

        if flask_app.config["ENV"] == "development":
            cluster_status.status = random.randint(0, 1)
        else:
            try:
                probe_result = requests.get(cluster_probe_url, timeout=2.50)
                cluster_status.status = (
                    1 if 200 <= probe_result.status_code < 300 else 0
                )
            except requests.RequestException as e:
                logger.exception(e)
                cluster_status.status = 0

        db.session.add(cluster_status)
        db.session.commit()


@celery.task
def fetch_cluster_request_counts(time_range: str = "30s") -> None:
    for cluster in flask_app.config["MIDL_CLUSTER_INFO"]:
        cluster_name, cluster_labels = cluster["name"], cluster["cluster_labels"]
        cluster_requests = RequestCount(cluster=cluster_name, time=datetime.now())

        if flask_app.config["ENV"] == "development":
            cluster_requests.count = random.randint(5000, 15000)
        else:
            loki_url = flask_app.config["MIDL_LOKI_URL"]
            loki_connect = LokiConnect(url=loki_url)
            loki_query = f"sum(count_over_time({{{cluster_labels}}}[{time_range}]))"
            try:
                loki_resp = loki_connect.query(query=loki_query)
                request_counts = (
                    loki_resp["data"]["result"][0]["value"][-1]
                    if len(loki_resp["data"]["result"]) > 0
                    else 0
                )
                cluster_requests.count = request_counts
            except Exception as e:
                logger.exception(e)
                cluster_requests.count = 0

        db.session.add(cluster_requests)
        db.session.commit()


@celery.task
def cleanup_status_data(hours: int = 72) -> None:
    oldest_data = datetime.now() - timedelta(hours=hours)
    # clean up ClusterStatus
    ClusterStatus.query.filter(ClusterStatus.created_at < oldest_data).delete()
    # clean up RequestCount
    RequestCount.query.filter(RequestCount.created_at < oldest_data).delete()

    db.session.commit()