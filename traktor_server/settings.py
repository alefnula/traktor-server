"""
Django settings for traktor project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import os
from pathlib import Path
from datetime import timedelta

from redis import ConnectionPool

from traktor_server import log
from traktor_server.config import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.secret_key

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.debug

ALLOWED_HOSTS = ["127.0.0.1", config.server_host]

URL_PREFIX = "" if config.url_prefix is None else f"/{config.url_prefix}"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "huey.contrib.djhuey",
    "django_simple_bulma",
    "rest_framework",
    "tea_django",
    "traktor",
    "traktor_server",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "traktor_server.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "traktor_server.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": f"django.db.backends.{config.db_engine}",
        "NAME": config.db_name,
        "USER": config.db_user,
        "PASSWORD": config.db_password,
        "HOST": config.db_host,
        "PORT": config.db_port,
    }
}


AUTH_USER_MODEL = "traktor.User"

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation"
        ".UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation"
        ".NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = config.timezone.zone

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGGING = log.create_logging_configuration(
    log_dir=config.log_dir, hosted=not config.debug
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = f"{URL_PREFIX}/static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_FINDERS = [
    # First add the two default Finders, since this will overwrite the default.
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    # Now add our custom SimpleBulma one.
    "django_simple_bulma.finders.SimpleBulmaFinder",
]

LOGIN_URL = f"{URL_PREFIX}/accounts/login/"
LOGIN_REDIRECT_URL = f"{URL_PREFIX}/"
LOGOUT_REDIRECT_URL = f"{URL_PREFIX}/"


# Rest Framework
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated"
    ],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "EXCEPTION_HANDLER": (
        "traktor_server.exception_handler.traktor_exception_handler"
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=365),
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": True,
    "AUTH_HEADER_TYPES": ("JWT",),
}


HUEY = {
    "name": "traktor_server",
    "connection": {
        "connection_pool": ConnectionPool.from_url(
            config.redis_url, max_connections=10
        )
    },
    "consumer": {
        "workers": 2,
        "worker_type": "process",
        "logfile": os.path.join(config.log_dir, "huey.log"),
    },
    "immediate": False,
    #
}
