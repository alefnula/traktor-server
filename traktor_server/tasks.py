from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task

from traktor.models import Task
from traktor_server.models import History


def create():
    for task in Task.objects.all():
        History.create(task)


@db_task()
def create_history():
    create()


@db_periodic_task(crontab("*/15"))
def create_history_periodic():
    create()
