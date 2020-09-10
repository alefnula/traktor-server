from django.http import Http404
from django.shortcuts import render

from traktor_server.models import Balance


def get_client_ip(request) -> str:
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0]
    else:
        return request.META.get("REMOTE_ADDR")


def metrics(request):
    if get_client_ip(request) != "127.0.0.1":
        raise Http404()

    return render(
        request,
        "traktor/prometheus.txt",
        {"balances": Balance.objects.all()},
        content_type="text/plain; charset=utf-8",
    )
