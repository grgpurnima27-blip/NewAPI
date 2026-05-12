# from pathlib import Path
# import os
# from django.core.mail import EmailMessage
# from dotenv import load_dotenv
# import dj_database_url

# load_dotenv(override=False)  

# BASE_DIR = Path(__file__).resolve().parent.parent


# # CORE SETTINGS

# SECRET_KEY = os.environ.get('SECRET_KEY')
# DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# ALLOWED_HOSTS = [
#     '127.0.0.1',
#     'localhost',
#     '.onrender.com',
# ]


# # INSTALLED APPS

# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'rest_framework',
#     'corsheaders',
#     'drf_yasg',
#     'rest_framework_simplejwt.token_blacklist',
#     'django_rest_passwordreset',
#     'books.apps.BooksConfig',
# ]


# # MIDDLEWARE

# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# ROOT_URLCONF = 'config.urls'


# # TEMPLATES

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [BASE_DIR / 'templates'],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# WSGI_APPLICATION = 'config.wsgi.application'


# # DATABASE

# DATABASES = {
#     'default': dj_database_url.config(
#         default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
#         conn_max_age=600,
#     )
# }


# # PASSWORD VALIDATION

# AUTH_PASSWORD_VALIDATORS = [
#     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
#     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# ]


# # REST FRAMEWORK

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
#     'PAGE_SIZE': 5,
# }


# # SWAGGER

# SWAGGER_SETTINGS = {
#     'USE_SESSION_AUTH': False,
#     'SECURITY_DEFINITIONS': {
#         'Bearer': {
#             'type': 'apiKey',
#             'name': 'Authorization',
#             'in': 'header',
#         }
#     },
# }


# # PASSWORD RESET

# DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE = False
# PASSWORD_RESET_CONFIRM_URL = 'reset-password/{token}/'


# # EMAIL CONFIG — SMTP (Gmail for Render)

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True

# EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')   
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  

# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# # BASE URL (Render production URL)
# BASE_URL = os.environ.get(
#     'BASE_URL',
#     'https://newapi-jgbv.onrender.com'
# )
# # EMAIL CONFIG - Mailjet API

# # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# # EMAIL_HOST = 'smtp.gmail.com'
# # EMAIL_PORT = 587
# # EMAIL_USE_TLS = True
# # EMAIL_USE_SSL = False
# # EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
# # EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
# # DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER')
# # # Mailjet API Keys
# # MAILJET_API_KEY = os.environ.get('MAILJET_API_KEY')
# # MAILJET_API_SECRET = os.environ.get('MAILJET_API_SECRET')
# # # RESEND_API_KEY = os.environ.get('RESEND_API_KEY')

# # BASE URL FOR EMAIL LINKS — FIXED
# BASE_URL = os.environ.get('BASE_URL', 'https://newapi-jgbv.onrender.com')


# # CORS CONFIG

# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True

# CORS_ALLOW_HEADERS = [
#     'authorization',
#     'content-type',
#     'accept',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
# ]

# CORS_ALLOW_METHODS = [
#     'DELETE',
#     'GET',
#     'OPTIONS',
#     'PATCH',
#     'POST',
#     'PUT',
# ]


# # LOGIN URL

# LOGIN_URL = '/admin/login/'


# # STATIC FILES

# STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# # from pathlib import Path
# # import os
# # from dotenv import load_dotenv
# # import dj_database_url

# # load_dotenv(override=False)

# # BASE_DIR = Path(__file__).resolve().parent.parent


# # # CORE SETTINGS

# # SECRET_KEY = os.environ.get('SECRET_KEY')
# # DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# # ALLOWED_HOSTS = [
# #     '127.0.0.1',
# #     'localhost',
# #     '.onrender.com',
# # ]


# # # INSTALLED APPS

# # INSTALLED_APPS = [
# #     'django.contrib.admin',
# #     'django.contrib.auth',
# #     'django.contrib.contenttypes',
# #     'django.contrib.sessions',
# #     'django.contrib.messages',
# #     'django.contrib.staticfiles',
# #     'rest_framework',
# #     'corsheaders',
# #     'drf_yasg',
# #     'rest_framework_simplejwt.token_blacklist',
# #     'django_rest_passwordreset',
# #     'books.apps.BooksConfig',
# # ]


# # # MIDDLEWARE

# # MIDDLEWARE = [
# #     'corsheaders.middleware.CorsMiddleware',
# #     'django.middleware.security.SecurityMiddleware',
# #     'whitenoise.middleware.WhiteNoiseMiddleware',
# #     'django.contrib.sessions.middleware.SessionMiddleware',
# #     'django.middleware.common.CommonMiddleware',
# #     'django.middleware.csrf.CsrfViewMiddleware',
# #     'django.contrib.auth.middleware.AuthenticationMiddleware',
# #     'django.contrib.messages.middleware.MessageMiddleware',
# #     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# # ]

# # ROOT_URLCONF = 'config.urls'


# # # TEMPLATES

# # TEMPLATES = [
# #     {
# #         'BACKEND': 'django.template.backends.django.DjangoTemplates',
# #         'DIRS': [BASE_DIR / 'templates'],
# #         'APP_DIRS': True,
# #         'OPTIONS': {
# #             'context_processors': [
# #                 'django.template.context_processors.request',
# #                 'django.contrib.auth.context_processors.auth',
# #                 'django.contrib.messages.context_processors.messages',
# #             ],
# #         },
# #     },
# # ]

# # WSGI_APPLICATION = 'config.wsgi.application'


# # # DATABASE

# # DATABASES = {
# #     'default': dj_database_url.config(
# #         default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
# #         conn_max_age=600,
# #     )
# # }


# # # PASSWORD VALIDATION

# # AUTH_PASSWORD_VALIDATORS = [
# #     {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
# #     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
# #     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
# #     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
# # ]


# # # REST FRAMEWORK

# # REST_FRAMEWORK = {
# #     'DEFAULT_AUTHENTICATION_CLASSES': (
# #         'rest_framework_simplejwt.authentication.JWTAuthentication',
# #     ),
# #     'DEFAULT_PERMISSION_CLASSES': (
# #         'rest_framework.permissions.IsAuthenticated',
# #     ),
# #     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
# #     'PAGE_SIZE': 5,
# # }


# # # SWAGGER

# # SWAGGER_SETTINGS = {
# #     'USE_SESSION_AUTH': False,
# #     'SECURITY_DEFINITIONS': {
# #         'Bearer': {
# #             'type': 'apiKey',
# #             'name': 'Authorization',
# #             'in': 'header',
# #         }
# #     },
# # }


# # # PASSWORD RESET

# # DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE = False
# # PASSWORD_RESET_CONFIRM_URL = 'reset-password/{token}/'


# # # EMAIL CONFIG — Mailjet REST API
# # # We use Mailjet's Python client directly (not Django's email backend).
# # # The variables below are read in views.py via settings.MAILJET_API_KEY etc.

# # MAILJET_API_KEY = os.environ.get('MAILJET_API_KEY')
# # MAILJET_API_SECRET = os.environ.get('MAILJET_API_SECRET')
# # MAILJET_SENDER_EMAIL = os.environ.get('MAILJET_SENDER_EMAIL', 'grgpurnima27@gmail.com')
# # MAILJET_SENDER_NAME = os.environ.get('MAILJET_SENDER_NAME', 'Book API')

# # # BASE URL used in email verification and password reset links
# # BASE_URL = os.environ.get('BASE_URL', 'https://newapi-jgbv.onrender.com')


# # # CORS CONFIG

# # CORS_ALLOW_ALL_ORIGINS = True
# # CORS_ALLOW_CREDENTIALS = True

# # CORS_ALLOW_HEADERS = [
# #     'authorization',
# #     'content-type',
# #     'accept',
# #     'origin',
# #     'user-agent',
# #     'x-csrftoken',
# # ]

# # CORS_ALLOW_METHODS = [
# #     'DELETE',
# #     'GET',
# #     'OPTIONS',
# #     'PATCH',
# #     'POST',
# #     'PUT',
# # ]


# # # LOGIN URL

# # LOGIN_URL = '/admin/login/'


# # # STATIC FILES

# # STATIC_URL = 'static/'
# # STATIC_ROOT = BASE_DIR / 'staticfiles'
# # STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent


# ================= CORE =================

SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.onrender.com',
]


# ================= APPS =================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'rest_framework_simplejwt.token_blacklist',
    'django_rest_passwordreset',

    'books.apps.BooksConfig',
]


# ================= MIDDLEWARE =================

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


# ================= DATABASE =================

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# ================= REST FRAMEWORK =================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}


# ================= SWAGGER =================

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


# ================= EMAIL (SMTP - GMAIL) =================

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# ================= PASSWORD RESET =================

DJANGO_REST_PASSWORDRESET_NO_INFORMATION_LEAKAGE = False
PASSWORD_RESET_CONFIRM_URL = 'reset-password/{token}/'


# ================= BASE URL =================

BASE_URL = os.environ.get('BASE_URL', 'https://your-app.onrender.com')


# ================= CORS =================

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


# ================= STATIC =================

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'