import logging

from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from traktor.models import Task
from traktor_server.models import Balance


logger = logging.getLogger(__name__)


def create(recalculate: bool = False):
    try:
        for task in Task.objects.all():
            Balance.create(task=task, recalculate=recalculate)
    except Exception:
        logger.exception("Creating balances failed!")


@db_task()
def create_balance():
    create()


@db_periodic_task(crontab("*/15"))
def create_balance_periodic():
    create()


@db_task()
def recreate_balance():
    create(recalculate=True)


@db_periodic_task(crontab(1, 0))
def recreate_balance_periodic():
    create(recalculate=True)
