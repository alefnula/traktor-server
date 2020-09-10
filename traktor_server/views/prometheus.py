from django.http import Http404
from django.db import connection
from django.shortcuts import render


SQL_QUERY = """
SELECT user.username AS user,
       project.name AS project,
       task.name AS task,
       max(history.timestamp) AS timestamp,
       history.cumulative_duration AS cumulative_duration,
       history.yearly_duration as yearly_duration,
       history.monthly_duration AS monthly_duration,
       history.weekly_duration AS weekly_duration
FROM traktor_server_history AS history
JOIN traktor_task AS task ON task.id = history.task_id
JOIN traktor_project AS project ON project.id = task.project_id
JOIN traktor_user AS user ON user.id = project.user_id
GROUP BY history.task_id
ORDER BY history.timestamp desc;
"""


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    else:
        return request.META.get("REMOTE_ADDR")


def fetch_data():
    with connection.cursor() as cursor:
        cursor.execute(SQL_QUERY)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def metrics(request):
    if get_client_ip(request) != "127.0.0.1":
        raise Http404()

    history = fetch_data()
    return render(
        request,
        "traktor/prometheus.txt",
        {"history": history},
        content_type="text/plain; charset=utf-8",
    )
