from pathlib import Path

import environ

env = environ.Env(
    DEBUG=(bool, False),
)

BASE_DIR = Path(__file__).resolve().parent.parent

env.read_env(BASE_DIR.parent / ".env")

SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "debug_toolbar",
]

LOCAL_APPS = [
    "common",
    "public",
    "users",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "common.middleware.loggers.ExceptionLoggerMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
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

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": env.db(),
    "extra": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "db.sqlite3",
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

USE_TZ = True

STATIC_ROOT = env.str("STATIC_ROOT", Path(BASE_DIR.parent / ".static"))

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)

SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)

SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)

INTERNAL_IPS = [
    "127.0.0.1",
    "localhost",
    "[::1]",
]

ERROR_LOG_FILE = env.str("ERROR_LOG_FILE", str(BASE_DIR.parent / "logs/error.log"))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app.verbose": {
            "format": "[{asctime}.{msecs:0<3.0f}] {levelname} {pathname}:{funcName}:{lineno} [{process}:{thread}] {message}",  # noqa: E501
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        },
    },
    "handlers": {
        "app.console": {
            "class": "logging.StreamHandler",
            "formatter": "app.verbose",
            "level": "DEBUG",
        },
        "app.file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "app.verbose",
            "level": "ERROR",
            "filename": ERROR_LOG_FILE,
            "maxBytes": 1024 * 1024 * 5,  # 5 MB
            "backupCount": 5,
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "app": {
            "handlers": [
                "app.console",
                "app.file",
            ],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

ADMIN_URL = env.str("ADMIN_URL", "admin/")

AUTH_USER_MODEL = "users.User"

Path(ERROR_LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
