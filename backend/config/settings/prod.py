from .base import *

DEBUG = False

# Persistent database connections — avoids reconnecting on every request
DATABASES['default']['CONN_MAX_AGE'] = env.int('DATABASE_CONN_MAX_AGE', default=600)

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Honor the 'X-Forwarded-Proto' header set by Nginx for SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)

AUTH_COOKIE_SECURE = env.bool('AUTH_COOKIE_SECURE', default=True)
SIMPLE_JWT['AUTH_COOKIE_SECURE'] = AUTH_COOKIE_SECURE
CSRF_COOKIE_SECURE = env.bool('CSRF_COOKIE_SECURE', default=True)
SESSION_COOKIE_SECURE = env.bool('SESSION_COOKIE_SECURE', default=True)

SECURE_HSTS_SECONDS = env.int('SECURE_HSTS_SECONDS', default=31536000)  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
