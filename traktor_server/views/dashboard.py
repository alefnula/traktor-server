import itertools
from copy import deepcopy
from datetime import date, timedelta


from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from traktor.models import Project


def rgb(hex):
    return f"rgb({int(hex[1:3], 16)}, {int(hex[3:5], 16)}, {int(hex[5:], 16)})"


DATE_FMT = "%Y-%m-%d"


def generate_dataset(slug, start_date):
    project = Project.get_by_slug(slug)
    project_dataset = {
        "label": project.name,
        "data": [0] * 31,
        "backgroundColor": rgb(project.color),
        "borderColor": rgb(project.color),
        "fill": False,
    }
    for entry in project.entry_set.filter(start_time__gte=start_date):
        diff = (entry.start_time.date() - start_date).days
        project_dataset["data"][diff] += entry.duration / 60
    return project_dataset


def sum_datasets(ds):
    result = []
    for i, ds in enumerate(ds):
        for j, value in enumerate(ds["data"]):
            if i == 0:
                result.append(value)
            else:
                result[j] += value
    return result


@login_required
def index(request):
    start_date = date.today() - timedelta(days=30)

    chart = {
        "type": "line",
        "data": {
            "labels": [
                d.strftime(DATE_FMT)
                for d in [(start_date + timedelta(days=i)) for i in range(31)]
            ],
            "datasets": [
                generate_dataset("piano", start_date),
                generate_dataset("guitar", start_date),
                generate_dataset("singing", start_date),
            ],
        },
        "options": {},
    }

    # Add cumulative daily practice
    chart["data"]["datasets"].append(
        {
            "label": "Cumulative daily practice",
            "data": sum_datasets(chart["data"]["datasets"]),
            "backgroundColor": rgb("#CCCCCC"),
            "borderColor": rgb("#CCCCCC"),
            "fill": False,
        }
    )

    cumsum_chart = deepcopy(chart)

    cumsum_chart["data"]["datasets"][0]["data"] = list(
        itertools.accumulate(cumsum_chart["data"]["datasets"][0]["data"])
    )
    cumsum_chart["data"]["datasets"][1]["data"] = list(
        itertools.accumulate(cumsum_chart["data"]["datasets"][1]["data"])
    )
    cumsum_chart["data"]["datasets"][2]["data"] = list(
        itertools.accumulate(cumsum_chart["data"]["datasets"][2]["data"])
    )
    cumsum_chart["data"]["datasets"][3]["data"] = list(
        itertools.accumulate(cumsum_chart["data"]["datasets"][3]["data"])
    )

    return render(
        request,
        "traktor/index.html",
        {"chart": chart, "cumsum_chart": cumsum_chart},
    )
