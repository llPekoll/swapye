import locale
import os
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

locale.setlocale(locale.LC_ALL, "fr_FR")

sentry_sdk.init(
    dsn="https://83786559d7d34785803ee9c718ef9471@o1066269.ingest.sentry.io/6058874",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

BACKEND_DNS = os.environ.get("BACKEND_DNS", "https://localhost")
HOME_DNS = os.environ.get("HOME_DNS", "https://localhost")
TERMINAL_DNS = os.environ.get("TERMINAL_DNS", "https://localhost")
DASHBOARD_DNS = os.environ.get("DASHBOARD_DNS", "https://localhost")
GAME_DNS = os.environ.get("GAME_DNS", "https://localhost")
WORKER_DNS = os.environ.get("WORKER_DNS", "https://localhost")
BOUNCER_API_KEY = os.environ.get("BOUNCER_API_KEY", "fasdfas2f23f3")

# SENDGRID_API_KEY = os.environ.get("STRIPE_SECRET_KEY")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "mamadou aie aie aie")

DEBUG = (
    os.environ.get("STATE", "TEST") == "DEV" or os.environ.get("STATE", "TEST") == "QA"
)
STATE = os.environ.get("STATE")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
    ),
}

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
ALLOWED_HOSTS = [
    os.environ.get("GAME_DNS", "https://localhost").replace("https://", ""),
    os.environ.get("BACKEND_DNS", "https://localhost").replace("https://", ""),
    os.environ.get("DASHBOARD_DNS", "https://localhost").replace("https://", ""),
    "127.0.0.1",
    "192.168.1.255",
    "192.168.1.87",
    "localhost",
    "testserver",
    "www.swapye.com",
    "swapye.com",
    "qa-api.swapye.fr",
    "www.swapye.fr",
    "swapye.fr",
    "vercel.app",
]

CORS_ALLOWED_ORIGINS = [
    os.environ.get("DASHBOARD_DNS", "http://localhost:5173"),
    "http://localhost:5173",
]


CORS_ORIGIN_WHITELIST = (
    os.environ.get("HOME_DNS", "http://localhost:5173"),
    os.environ.get("BACKEND_DNS", "http://localhost:5173"),
    os.environ.get("DASHBOARD_DNS", "http://localhost:5173"),
    "http://localhost:5173" "http://192.168.1.255:5173" "http://192.168.1.87:3002",
    "http://192.168.1.87:3002",
    "http://192.168.1.87:3001",
    "http://192.168.1.87:8000",
    "http://192.168.1.255:5173",
    "https://www.swapye.com",
    "https://*.swapye.fr",
    "https://*.swapye.com",
    "https://*.swapye.work",
)

CSRF_TRUSTED_ORIGINS = [
    "https://*.swapye.fr",
    "https://*.swapye.com",
    "https://*.swapye.work",
    "https://*.127.0.0.1",
]

INTERNAL_IPS = [
    "127.0.0.1",
]

INSTALLED_APPS = [
    "authie",
    "dash",
    "trads",
    "games",
    "tools",
    "ckeditor",
    "debug_toolbar",
    "corsheaders",
    "background_task",
    "rest_framework",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]


ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
        ],
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

WSGI_APPLICATION = "backend.wsgi.application"


if STATE == "TEST":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "backend",
            "USER": "postgres",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "5432",
        },
        "trad": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "backend",
            "USER": "postgres",
            "PASSWORD": "",
            "HOST": "localhost",
            "PORT": "5432",
        },
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": os.environ.get("DB_DATABASE", "http://localhost:5173"),
            "USER": os.environ.get("DB_USERNAME", "http://localhost:5173"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "http://localhost:5173"),
            "HOST": os.environ.get("DB_HOST", "http://localhost:5173"),
            "PORT": os.environ.get("DB_PORT", "http://localhost:5173"),
            "OPTIONS": {
                "sslmode": "require",
            },
        },
        "trad": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "swapye_trad",
            "USER": os.environ.get("DB_USERNAME", "http://localhost:5173"),
            "PASSWORD": os.environ.get("DB_PASSWORD", "http://localhost:5173"),
            "HOST": os.environ.get("DB_HOST", "http://localhost:5173"),
            "PORT": os.environ.get("DB_PORT", "http://localhost:5173"),
            "OPTIONS": {
                "sslmode": "require",
            },
        },
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "https://bearwallet.fra1.digitaloceanspaces.com/django/static/"
# STATIC_URL = "/static"
# STATIC_ROOT = "static"
# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

AWS_ACCESS_KEY_ID = os.environ.get("SPACES_KEY", "SIBCNRIXZMVE5X5OHMN8")
AWS_SECRET_ACCESS_KEY = os.environ.get("SPACES_SECRET", "SIBCNRIXZMVE5X5OHMN8")
AWS_STORAGE_BUCKET_NAME = os.environ.get("BUCKET", "mamadou")
AWS_S3_REGION_NAME = os.environ.get("REGION_NAME", "fr")
AWS_S3_ENDPOINT_URL = os.environ.get(
    "ENDPOINT_URL", "https://fra1.digitaloceanspaces.com"
)
AWS_S3_ROOT = os.environ.get("S3_ROOT", "test")
AWS_CDN_URL = os.getenv("CDN_URL", "https://fra1.digitaloceanspaces.com")
AWS_DEFAULT_ACL = "public-read"

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


import logging

LOGLEVEL = os.environ.get("LOGLEVEL", "info").upper()
LOGGING_CONFIG = None
import logging.config

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "main_format": {
            "format": "[%(levelname)s] %(asctime)s %(module)s %(funcName)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "main_format",
            "level": "DEBUG",
        },
        "file": {
            "level": "INFO",
            "formatter": "main_format",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{BASE_DIR}/django.log",
            "maxBytes": 5242880,
            "encoding": "utf-8",
            "backupCount": 3,
        },
    },
    "loggers": {
        "app": {
            "level": LOGLEVEL,
            # "handlers": ["console", "file"],
            "handlers": ["console"],
        },
    },
}

logging.config.dictConfig(LOGGING)
