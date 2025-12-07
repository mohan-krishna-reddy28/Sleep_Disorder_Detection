"""
Django settings for FRONTEND project.
"""

from pathlib import Path
import os
import sys

# ---------------------------------------------------------
# BASE DIRECTORY SETTINGS
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent    # Path to FRONTEND folder
PROJECT_ROOT = BASE_DIR.parent                # Path to Sleep_disorder folder
BACKEND_DIR = PROJECT_ROOT / "BACKEND"         # Path to BACKEND folder 

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
# ---------------------------------------------------------
# STATIC FILES (CSS, JS, Images)
# ---------------------------------------------------------
STATIC_URL = "/static/"

STATICFILES_DIRS = [
    PROJECT_ROOT / "static", # <--- **FIX 1: Add the top-level static directory**
    PROJECT_ROOT / "sleep_app" / "static", # Keep if you have app-specific static files
]

STATIC_ROOT = PROJECT_ROOT / "staticfiles"

# ---------------------------------------------------------
# DEFAULT FIELD TYPE
# ---------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
# ... other settings ...

# ---------------------------------------------------------
# STATIC FILES (CSS, JS, Images)
# ---------------------------------------------------------
# ... existing STATIC_URL, STATICFILES_DIRS, STATIC_ROOT ...

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage" # Add this line