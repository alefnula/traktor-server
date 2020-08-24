"""traktor URL Configuration."""

from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from traktor_server.config import config


urlpatterns = [
    # admin
    path("admin/", admin.site.urls),
    # auth
    path("accounts/", include("django.contrib.auth.urls")),
    # api v0
    path("api/v0/", include("traktor_server.views.api.v0.urls")),
]

if config.url_prefix is None:
    urlpatterns += staticfiles_urlpatterns()
else:
    urlpatterns = [
        path(f"{config.url_prefix}/", include(urlpatterns))
    ] + staticfiles_urlpatterns()
