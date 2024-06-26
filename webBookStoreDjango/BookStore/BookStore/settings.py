"""
Django settings for BookStore project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
from pathlib import Path
import os.path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j^1mgx_llc50-jbk0d9d__+uk)f^*03k#gd*h5ajmwilh=a_w-'

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
    'book',
    'cart',
    'mobile',
    'customer',
    'order',
    'catalog',
    'app',
    'search',
    'manager',
    'clothes',
    'shipment',
    'payment',
    'notification',
    'djongo',
    'rest_framework',
    # 'rest_framework_simplejwt',
    # 'django.contrib.flatpages',
    # 'django.contrib.sites',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
]

ROOT_URLCONF = 'BookStore.urls'

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
                'django.template.context_processors.media',
                # thêm thông tin vào context của template trước khi nó được render.
                'app.context_processors.bookstore',
            ],
        },
    },
]

WSGI_APPLICATION = 'BookStore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "library",
        "USER": "root",
        # "PASSWORD": "anhgdt1710",
        "PASSWORD": "anh1710gdt",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    },
    "customer": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "customer",
        "USER": "root",
        # "PASSWORD": "anhgdt1710",
        "PASSWORD": "anh1710gdt",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    },
    "manager": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "manager",
        "USER": "root",
        # "PASSWORD": "anhgdt1710",
        "PASSWORD": "anh1710gdt",
        "HOST": "127.0.0.1",
        "PORT": "3306",
    },
    'order':{
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': 'order',
        'USER': 'postgres',
        'PASSWORD': 'anh1710gdt',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'payment':{
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': 'payment',
        'USER': 'postgres',
        'PASSWORD': 'anh1710gdt',
        'HOST': 'localhost',
        'PORT': '5432',
    },
    'shipment':{
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': 'shipment',
        'USER': 'postgres',
        'PASSWORD': 'anh1710gdt',
        'HOST': 'localhost',
        'PORT': '5432',
    },

    'search': {
        'ENGINE': 'djongo',
        'NAME':'search',
        'HOST': 'localhost',
        'PORT': 27017,
    },

}

DATABASE_ROUTERS = [
    'cart.routers.CartRouter',
    'manager.routers.ManagerRouter',
    'customer.routers.CustomerRouter',
    'search.routers.SearchRouter',
    'order.routers.OrderRouter',
    'payment.routers.PaymentRouter',
    # 'shipment.routers.ShipmentRouter',
]

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
ALGORITHM = "HS256"
SIGNING_KEY = "BAT_CHANH_DAO"

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')
MEDIA_URL = '/images/'

CART_SESSION_ID = 'cart'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SITE_NAME = 'Library of 3 original' # tên của trang web. {{site_name}}
# Các từ khóa meta (meta keywords) được sử dụng để cung cấp thông tin về nội dung của trang web cho các công cụ tìm kiếm
META_KEYWORDS = 'books, literature, reading, bookstore'
# Mô tả meta (meta description) là một phần quan trọng của SEO, nó cung cấp mô tả ngắn gọn về nội dung của trang web để hiển thị trong kết quả tìm kiếm.
META_DESCRIPTION = 'Explore a wide range of books at our bookstore. Find the latest literature, fiction, non-fiction, and more for an immersive reading experience.'

# Cookie name. sử dụng để theo dõi phiên làm việc của người dùng.
SESSION_COOKIE_NAME = 'sessionid'
# The module to store sessions data. đối tượng lưu trữ phiên làm việc.
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Age of cookie, in seconds (default: 1 weeks).
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7
# Xác định xem cookie phiên làm việc có hết hạn khi trình duyệt đóng hay không.
# Nếu đặt là True, cookie sẽ hết hạn khi trình duyệt đóng
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
 # Xác định xem cookie phiên làm việc chỉ được gửi qua kết nối bảo mật (https) hay không.
# Đối với giá trị False, cookie cũng sẽ được gửi qua kết nối không an toàn (http).
SESSION_COOKIE_SECURE = False
# ID của trang web trong trường hợp có nhiều trang web trong cùng một ứng dụng Django.
SITE_ID = 1
# Số lượng sản phẩm hiển thị trên mỗi trang khi hiển thị danh sách sản phẩm.
PRODUCTS_PER_PAGE = 12

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

