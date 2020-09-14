import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from traktor.models import Task
from traktor_server.models import Balance


logger = logging.getLogger(__name__)


def create():
    try:
        for task in Task.objects.all():
            Balance.create(task)
    except Exception:
        logger.exception("Creating balances failed!")


@db_task()
def create_balance():
    create()


@db_periodic_task(crontab("*/15"))
def create_balance_periodic():
    create()
