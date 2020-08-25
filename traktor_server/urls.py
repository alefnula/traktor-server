"""traktor URL Configuration."""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from traktor_server.config import config
from traktor_server.views import dashboard


urlpatterns = [
    path("", dashboard.index, name="ts.index"),
    # auth
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    # admin
    path("admin/", admin.site.urls),
    # api v0
    path("api/v0/", include("traktor_server.views.api.v0.urls")),
]

if config.url_prefix is None:
    urlpatterns += staticfiles_urlpatterns()
else:
    urlpatterns = [
        path(f"{config.url_prefix}/", include(urlpatterns))
    ] + staticfiles_urlpatterns()
