# coding:utf-8

import os

import config
from config import Path, DjangoDatabase, FundcDatabase

DEBUG = config.DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DjangoDatabase.NAME,
        'USER': DjangoDatabase.USER,
        'PASSWORD': DjangoDatabase.PASSWORD,
        'HOST': DjangoDatabase.HOST,
        'PORT': DjangoDatabase.PORT,
    },
    FundcDatabase.ROUTERNAME: {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': FundcDatabase.NAME,
        'USER': FundcDatabase.USER,
        'PASSWORD': FundcDatabase.PASSWORD,
        'HOST': FundcDatabase.HOST,
        'PORT': FundcDatabase.PORT,
    },
}

DATABASE_ROUTERS = ['fundc.models.router.Router']

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh_CN.UTF-8'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

DATE_FORMAT = 'Y-m-d'
DATETIME_FORMAT = 'Y-m-d H:i:s'
TIME_FORMAT = 'H:i:s'
YEAR_MONTH_FORMAT = 'Y-m'
MONTH_DAY_FORMAT = 'm-d'
SHORT_DATE_FORMAT = 'Y-m-d'
SHORT_DATETIME_FORMAT = 'Y-m-d H:i:s'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(Path.WEB, 'media')
STATIC_ROOT = os.path.join(Path.WEB, 'static')

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'fundc68e1bi(8r3bvui*%%10au++%$#ace0*eh-t7^-k1t33lpt'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'fundc.urls'

TEMPLATE_DIRS = (
    os.path.join(Path.WEB, 'templates')
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.request",
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
)