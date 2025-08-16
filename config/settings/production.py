# from config.settings.base import *

# DEBUG = False


from config.settings.base import *
import os

# Chạy production
DEBUG = False

# ALLOWED_HOSTS từ env hoặc mặc định '*'
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Database: port phải đúng với container internal của Postgres
DATABASES['default'].update({
    'NAME': os.getenv('DB_NAME', 'stock_predict_db'),
    'USER': os.getenv('DB_USER', 'postgres'),
    'PASSWORD': os.getenv('DB_PASSWORD', 'postgrespass'),
    'HOST': os.getenv('DB_HOST', 'stock-predict-postgres'),
    'PORT': int(os.getenv('DB_PORT', 5432)),  # lưu ý 5432 là default trong container
})

# Cache production (nếu chưa dùng Memcached, comment block này)
if ENVIRONMENT == 'production':
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
        'level': 'DEBUG',  # debug level để thấy lỗi boot
    },
}
