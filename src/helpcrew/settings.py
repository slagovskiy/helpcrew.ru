import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd party apps

    # my apps
    'helpcrew.userext',
    'helpcrew.toolbox',
    'helpcrew.taskqueue',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # my middleware
    'helpcrew.toolbox.middleware.ClearTempMiddleware',
]

ROOT_URLCONF = 'helpcrew.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'helpcrew.wsgi.application'

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


SENDFILE_BACKEND = 'sendfile.backends.simple'

LOGIN_URL = r'/admin/login/'

AUTH_USER_MODEL = 'userext.User'

try:
    from .settings_local import *
except ImportError:
    pass

if not SECRET_KEY:
    raise Exception('You must provide SECRET_KEY value in settings_local.py')

'''
# settings_local.py

from .settings import BASE_DIR
import os

DEBUG = True
SECRET_KEY = '-vop18rtmr(sy-1f)74-5@=mv(_9zl@xa$7=7mw4&nsq^jo)sy'
ALLOWED_HOSTS = []

# email
DEFAULT_FROM_EMAIL = 'noreply@helpcrew.ru'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'noreply@helpcrew.ru'
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = '[helpcrew]'

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

UPLOAD_URL = '/media/'
UPLOAD_DIR = os.path.join(BASE_DIR, 'media')

WORKER_PID = os.path.join(BASE_DIR, 'worker.pid')

SITE_URL = 'http://127.0.0.1:8000'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
'''