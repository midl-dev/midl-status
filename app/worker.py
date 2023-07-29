from celery import Celery

# from celery.schedules import crontab
from celery.utils.log import get_task_logger

from app.main import create_app

logger = get_task_logger(__name__)


def create_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    return celery


flask_app = create_app()
celery = create_celery(flask_app)


@celery.task
def test_task():
    logger.debug("hello world")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls reverse_messages every 10 seconds.
    sender.add_periodic_task(5.0, test_task, name="test task")
