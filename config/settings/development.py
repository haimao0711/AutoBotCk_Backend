from config.settings.base import *
import os

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,0.0.0.0,*").split(",")

# Database: đồng bộ với POSTGRES_* env
DATABASES['default'].update({
    'NAME': os.getenv('POSTGRES_DB', 'stockdb'),
    'USER': os.getenv('POSTGRES_USER', 'myuser'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'mypassword'),
    'HOST': os.getenv('POSTGRES_HOST', 'localhost'),
    'PORT': int(os.getenv('POSTGRES_PORT', 5432)),
})

if os.getenv('DJANGO_ENV') == 'production':
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }

SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
