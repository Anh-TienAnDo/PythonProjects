"""
Django settings for ThuVien3Goc project.

Generated by 'django-admin startproject' using Django 4.0.10.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os.path
from datetime import timedelta, datetime
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-$^@helba=5keor7d=k$9pkogkyno7h%3n(67d4wuz00a!ba+gk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    ## Custom App
    'core',
    'cart',
    'order',
    'product',
    'shipment',
    'user',
    'notification',
    'search',
    'rest_framework',
    # 'ratelimit',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 3600  # 1 hour
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True


ROOT_URLCONF = 'ThuVien3Goc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ThuVien3Goc.wsgi.application'

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "thuvien3goc_cache_table",  # Tên của bảng trong cơ sở dữ liệu
    }
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "thuvien3goc",
        "USER": "root",
        "PASSWORD": "anh1710gdt",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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


SIMPLE_JWT = {
    # Xác định thời gian sống của token truy cập và token làm mới
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    # xác minh HMAC đối xứng thuật toán sau: 'HS256', 'HS384', 'HS512' -> SIGNING_KEY sẽ được sử dụng làm cả khóa ký và khóa xác minh
    # xác minh RSA không đối xứng, có thể sử dụng các thuật toán sau: 'RS256', 'RS384', 'RS512'. Khi thuật toán RSA được chọn, cài đặt SIGNING_KEY phải được đặt thành chuỗi chứa khóa riêng RSA
    "ALGORITHM": "HS256",
    # Khóa ký được sử dụng để ký nội dung của mã thông báo được tạo
    "SIGNING_KEY": "BAT_CHANH_DAO",
}

DATABASE_ROUTERS = []

FILE_UPLOAD_HANDLERS = [
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
]

AUTH_USER_MODEL = "user.Account"


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'vi'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/' # css, js, image, mp3, mp4, pdf...
STATIC_ROOT = os.path.join(BASE_DIR, 'static/images/')
MEDIA_URL = 'media/' # jpg, png of user
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

PRODUCT_TYPE = {
    'USB': 'USB',
    'MEMORY_STICK': 'MemoryStick',
    'LOUDSPEAKER': 'Loudspeaker',        
}

MEDIASOCIAL_TYPE = ['sayings', 'audio-book', 'video']

CART_SESSION_ID = 'cart'

SESSION_COOKIE_AGE = 60 * 60 * 24
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_DOMAIN = None
SESSION_COOKIE_SECURE = False
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'lea81807@gmail.com'
EMAIL_HOST_PASSWORD = 'fnvx lqhj cywo qqos'

PAYPAL = {
    'CLIENT_ID': 'AfDPoHI56R2XNvxJrjVwg7I70dUedQj3M-c2eQdMF6np8iSd4qHhJ0PECb1bGC7X71GwBA1jDd4HhCtf',
    'CLIENT_SECRET': 'EFJxZgsb2kLXFya29eoKhvVK8MFaYV0QOYm8jQ2w0mc6GT7CiugBvwKPS-MaYYhU6oIkFIZ6ioZsMWYa',
}

# log_filename = f'debug_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '{levelname} {asctime} {module} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{levelname} {message}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': log_filename,
#             'formatter': 'verbose',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

ITEMS_PER_PAGE = 1
ITEMS_LIMIT = 48
