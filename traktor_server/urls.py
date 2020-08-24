"""traktor URL Configuration."""

from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from traktor_server.config import config


urlpatterns = [
    # admin
    path(f"{config.url_prefix}admin/", admin.site.urls),
    # auth
    path(f"{config.url_prefix}accounts/", include("django.contrib.auth.urls")),
    # api v0
    path(
        f"{config.url_prefix}api/v0/",
        include("traktor_server.views.api.v0.urls"),
    ),
] + staticfiles_urlpatterns()
