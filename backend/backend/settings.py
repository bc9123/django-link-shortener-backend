import os
import dj_database_url
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Application definition

INSTALLED_APPS = [
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'corsheaders',
  'rest_framework',
  'rest_framework_simplejwt.token_blacklist',
  'shortener',
  'authentication',
]

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
  {
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
      'context_processors': [
        'django.template.context_processors.debug',
        'django.template.context_processors.request',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
      ],
    },
  },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database configuration

DATABASES = {
  'default': dj_database_url.config(conn_max_age=600)
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
  {
    'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
  },
  {
    'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
  },
]

# Internationalization

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model

AUTH_USER_MODEL = 'authentication.User'

# CORS settings

CORS_ALLOWED_ORIGINS = os.environ.get(
  'CORS_ALLOWED_ORIGINS',
  'http://localhost:5173,http://127.0.0.1:5173'
).split(',')

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = [
  'content-type',
  'authorization',
  'x-csrftoken',
]

CORS_ALLOW_METHODS = [
  'GET',
  'POST',
  'PUT',
  'DELETE',
  'OPTIONS',
]

# CSRF trusted origins (for HTTPS setups)

CSRF_TRUSTED_ORIGINS = os.environ.get(
  'CSRF_TRUSTED_ORIGINS',
  ''
).split(',')

# Rest framework settings

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': [
    'rest_framework_simplejwt.authentication.JWTAuthentication',
  ],
  'DEFAULT_THROTTLE_CLASSES': [
    'rest_framework.throttling.UserRateThrottle',
  ],
  'DEFAULT_THROTTLE_RATES': {
    'user': '1000/day',
  },
}

# JWT settings

SIMPLE_JWT = {
  "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
  "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
  "ROTATE_REFRESH_TOKENS": True,
  "BLACKLIST_AFTER_ROTATION": True,
  "UPDATE_LAST_LOGIN": False,

  "ALGORITHM": "HS256",
  "SIGNING_KEY": SECRET_KEY,

  "AUTH_HEADER_TYPES": ("Bearer",),
  "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
  "USER_ID_FIELD": "id",
  "USER_ID_CLAIM": "user_id",
  "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

  "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
  "TOKEN_TYPE_CLAIM": "token_type",
  "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

  "JTI_CLAIM": "jti",

  "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
  "SLIDING_TOKEN_LIFETIME": timedelta(days=30),
  "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=30),

  "TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainPairSerializer",
  "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
  "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
  "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
  "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
  "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

# Logging settings

LOGGING = {
  'version': 1,
  'disable_existing_loggers': False,
  'handlers': {
    'file': {
      'level': 'ERROR',
      'class': 'logging.FileHandler',
      'filename': BASE_DIR / 'logs' / 'errors.log',
    },
  },
  'loggers': {
    'django': {
      'handlers': ['file'],
      'level': 'ERROR',
      'propagate': True,
    },
  },
}

# Domain for shortener (default fallback)

DEFAULT_DOMAIN = os.getenv('DEFAULT_DOMAIN', 'http://127.0.0.1:8000')

# Security settings

SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
X_FRAME_OPTIONS = 'DENY'
