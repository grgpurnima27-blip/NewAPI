from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url
import cloudinary

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# CORE

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.onrender.com',
]


# APPS

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cloudinary',
    'cloudinary_storage',

    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'rest_framework_simplejwt.token_blacklist',
    'django_rest_passwordreset',

    'books.apps.BooksConfig',
]


# MIDDLEWARE

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'config.urls'


# TEMPLATES

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'config.wsgi.application'


# DATABASE

DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    print("❌ DATABASE_URL is missing!")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# STATIC FILES

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# CLOUDINARY — explicit config so credentials are always applied

CLOUDINARY_CLOUD_NAME = os.environ.get('CLOUDINARY_CLOUD_NAME')
CLOUDINARY_API_KEY    = os.environ.get('CLOUDINARY_API_KEY')
CLOUDINARY_API_SECRET = os.environ.get('CLOUDINARY_API_SECRET')

cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD_NAME,
    api_key    = CLOUDINARY_API_KEY,
    api_secret = CLOUDINARY_API_SECRET,
    secure     = True,
)

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': CLOUDINARY_CLOUD_NAME,
    'API_KEY':    CLOUDINARY_API_KEY,
    'API_SECRET': CLOUDINARY_API_SECRET,
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


# REST FRAMEWORK

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# SWAGGER

SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        }
    },
}


# EMAIL (RESEND)

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    "onboarding@resend.dev"
)


# BASE URL

BASE_URL = os.environ.get("BASE_URL", "https://newapi-jgbv.onrender.com")


# PASSWORD RESET

DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE = False
PASSWORD_RESET_CONFIRM_URL = 'reset-password/{token}/'


# SECURITY / CORS

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'