import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'agFJ-Od93BE?>U4IQ1%PntKb8L^N&CfoumDs2@TkwSZ7<WV0xYRl$vyri*AG'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'player.apps.PlayerConfig',
    'song.apps.SongConfig',
    'plot.apps.PlotConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_otp',
    'django_otp.plugins.otp_totp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'desert.middleware.RateLimitMiddleware',
    'desert.middleware.ServerSafeGuardMiddleware',
    'desert.middleware.UserAgentMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

CSRF_COOKIE_SECURE = True

ROOT_URLCONF = 'desert.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]

WSGI_APPLICATION = 'desert.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': 'db',
        'PORT': '5432',
        'NAME': 'desert',
        'USER': 'desert',
        'PASSWORD': 'Desert_internal_stuff_22',
    }
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

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379',
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

# Need to be True in production
SESSION_COOKIE_SECURE = False

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale/')
]

LANGUAGES = (
    ('en-us', 'English'),
    ('zh-Hans', '中文'),
)

LANGUAGE_COOKIE_NAME = 'lang'

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'player.Player'

# Cloud Tencent COS Auth
COS_SECRET_ID = 'AKIDjIbdPu86oFQKxJOCizyg7IDsHPIuEH5b'
COS_SECRET_KEY = 'HH1TeYBYfvvgANJyMTJsBDySgdJjupTp'
BUCKET = 'desert-1258493860'
REGION = 'ap-shanghai'

# Email Auth
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'luo_evan@163.com'
EMAIL_HOST_PASSWORD = 'HDUPUHSCXOOAJXZJ'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# Need to be edited every version
API_VERSION = 'v1.0.1-M1'

# Rate limit
REQUEST_LIMIT_TIME = 600
REQUEST_LIMIT = 300

# Need to be True when operate in Admin Site
SAFEGUARD_MODE = True
