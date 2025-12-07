"""
Django settings for FRONTEND project.
"""

from pathlib import Path
import os
import sys

# ---------------------------------------------------------
# BASE DIRECTORY SETTINGS
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent     # Sleep_disorder/FRONTEND
PROJECT_ROOT = BASE_DIR.parent                        # Sleep_disorder/
BACKEND_DIR = PROJECT_ROOT / "BACKEND"                # Sleep_disorder/BACKEND

# Make BACKEND importable (for model_loader.py)
sys.path.append(str(BACKEND_DIR))

# ---------------------------------------------------------
# SECURITY & DEBUG SETTINGS
# ---------------------------------------------------------
SECRET_KEY = "django-insecure-zcbv9(=x58fjpdwh$w8eq=sq9dse98)&^nj-ofjb9j&=vdd#1l"

DEBUG = True  # Render overrides this in production

ALLOWED_HOSTS = ["*"]  # For local + Render

# ---------------------------------------------------------
# APPLICATIONS
# ---------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "sleep_app",
]

# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------
# URL & WSGI SETTINGS
# ---------------------------------------------------------
ROOT_URLCONF = "FRONTEND.urls"
WSGI_APPLICATION = "FRONTEND.wsgi.application"

# ---------------------------------------------------------
# TEMPLATE SETTINGS
# Global templates folder: Sleep_disorder/templates
# ---------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_ROOT / "templates"], 
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": PROJECT_ROOT / "db.sqlite3",  # DB in main folder
    }
}

# ---------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# STATIC FILES (CSS, JS, Images)
# Works on Local + Render
# ---------------------------------------------------------
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    PROJECT_ROOT / "sleep_app" / "static",  # global/static inside app
]

STATIC_ROOT = PROJECT_ROOT / "staticfiles"  # Render will collect files here

# ---------------------------------------------------------
# DEFAULT FIELD TYPE
# ---------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
