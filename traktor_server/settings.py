"""
Django settings for traktor project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta

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

ALLOWED_HOSTS = [config.server_host]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_tea",
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

STATIC_URL = (
    "/static/"
    if config.url_prefix is None
    else f"/{config.url_prefix}/static/"
)

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
        "rest_framework_jwt.authentication.JSONWebTokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "EXCEPTION_HANDLER": (
        "traktor_server.exception_handler.traktor_exception_handler"
    ),
}

JWT_AUTH = {
    "JWT_SECRET_KEY": SECRET_KEY,
    "JWT_ALGORITHM": "HS256",
    "JWT_VERIFY": True,
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_EXPIRATION_DELTA": timedelta(days=7),
    "JWT_ALLOW_REFRESH": True,
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=30),
}
