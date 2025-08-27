# from config.settings.base import *
# import os

# # Chạy production
# DEBUG = False

# # ALLOWED_HOSTS từ env hoặc mặc định '*'
# ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# # Database: phải khớp với Postgres container
# DATABASES['default'].update({
#     'NAME': os.getenv('DB_NAME', 'stockdb'),     
#     'USER': os.getenv('DB_USER', 'myuser'),        
#     'PASSWORD': os.getenv('DB_PASSWORD', 'mypassword'), 
#     'HOST': os.getenv('DB_HOST', 'stock-predict-postgres'),
#     'PORT': int(os.getenv('DB_PORT', 5432)),  
# })

# # Cache production (nếu chưa dùng Memcached, comment block này)
# if os.getenv('DJANGO_ENV') == 'production':
#     CACHES['default'] = {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }

# # Security headers cơ bản
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# X_FRAME_OPTIONS = 'DENY'

# # Logging để debug Gunicorn nếu crash
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'root': {
#         'handlers': ['console'],
#         'level': 'DEBUG',  # debug level để thấy lỗi boot
#     },
# }

from config.settings.base import *
import os

DEBUG = False

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

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
