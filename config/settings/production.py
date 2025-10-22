from config.settings.base import *
import os

DEBUG = False

# Đặt cứng ALLOWED_HOSTS cho production
ALLOWED_HOSTS = [
    "14.225.253.51",
    "autobotchungkhoan.pro.vn",
    "www.autobotchungkhoan.pro.vn",
    "localhost",
    "0.0.0.0",
]

# Database: đồng bộ với POSTGRES_* env (qua PgBouncer)
DATABASES['default'].update({
    'NAME': os.getenv('POSTGRES_DB', 'stockdb'),
    'USER': os.getenv('POSTGRES_USER', 'myuser'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'mypassword'),
    'HOST': os.getenv('POSTGRES_HOST', 'pgbouncer'),
    'PORT': int(os.getenv('POSTGRES_PORT', 6432)),
})

# Cache (production dùng locmem nếu chưa có memcached/redis)
if os.getenv('DJANGO_ENV') == 'production':
    CACHES['default'] = {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }

# Security headers cơ bản
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Logging để debug Gunicorn nếu crash
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
