from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# =========================
# CORE SETTINGS
# =========================
SECRET_KEY = os.environ.get('SECRET_KEY')
# EMAIL CONFIG (GMAIL)
# =========================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

EMAIL_HOST_USER = 'grgpurnima27@gmail.com'
EMAIL_HOST_PASSWORD = 'wpzq inym wvmj izxg'

DEFAULT_FROM_EMAIL = 'grgpurnima27@gmail.com'

# =========================
# BASE URL FOR EMAIL LINKS
# =========================

BASE_URL = os.environ.get('BASE_URL', 'http://192.168.18.181:3000')

# =========================
# CORS CONFIG
# =========================
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
    'authorization',
    'content-type',
    'accept',
    'origin',
    'user-agent',
    'x-csrftoken',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# =========================
# LOGIN URL
# =========================
LOGIN_URL = '/admin/login/'

# =========================
# STATIC FILES (RENDER)
# =========================
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'