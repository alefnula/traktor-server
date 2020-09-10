from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from traktor.models import Task
from traktor_server.models import Balance


def create():
    for task in Task.objects.all():
        Balance.create(task)


@db_task()
def create_balance():
    create()


@db_periodic_task(crontab("*/15"))
def create_balance_periodic():
    create()
