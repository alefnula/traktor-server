import logging

from django.conf import settings
from django.http import JsonResponse
from rest_framework import status as http_statuses
from tea_django.exception_handler import tea_django_exception_handler

from traktor import errors


logger = logging.getLogger(__name__)


def traktor_exception_handler(exc, context):
    if settings.DEBUG:
        logger.exception("Traktor exception handler.")
    else:
        logger.error("Traktor exception handler. Error: %s", exc)

    if isinstance(exc, errors.TimerIsNotRunning):
        data = {"error": str(exc)}
        status = http_statuses.HTTP_404_NOT_FOUND
        return JsonResponse(data, status=status)

    return tea_django_exception_handler(exc=exc, context=context)
