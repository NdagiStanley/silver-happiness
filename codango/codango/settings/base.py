"""
Django settings for codango project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from __future__ import absolute_import
import datetime
import os
import cloudinary

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
from django.contrib.messages import constants as message_constants
from celery.schedules import crontab


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BOWER_INSTALLED_APPS = (
    'mdi',
    'moment',
    'jquery',
    'bootstrap',
    'ace-builds',
)

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'static')


ENDLESS_PAGINATION_LOADING = """<img src="/static/img/ajax-loader.gif" alt="loading"/>"""

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'resources',
    'userprofile',
    'comments',
    'votes',
    'pairprogram',
    'bootstrapform',
    'cloudinary',
    'djangobower',
    'endless_pagination',
    'djcelery',
    'rest_framework',
    'social.apps.django_app.default',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'middleware.activity.ActivityMiddleWare',
    'middleware.navigation.NavigationMiddleWare',
    'middleware.resource.PopularResourcesMiddleware',
    'middleware.logout.SessionIdleTimeout',
)

ROOT_URLCONF = 'codango.urls'

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

AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home'
SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False
SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('SOCIAL_AUTH_FACEBOOK_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('SOCIAL_AUTH_FACEBOOK_SECRET')

WSGI_APPLICATION = 'codango.wsgi.application'

# REST
REST_FRAMEWORK = {
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

STATIC_URL = '/static/'

APPEND_SLASH = False

STATIC_ROOT = 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

cloudinary.config(
    cloud_name=os.getenv('cloud_name'),
    api_key=os.getenv('api_key'),
    api_secret=os.getenv('api_secret')
)

# custom message tag for django messaging middleware
MESSAGE_TAGS = {
    message_constants.ERROR: 'danger'
}

# Custom Email
ADMIN_EMAIL = 'stanley.ndagi@andela.com'
CODANGO_EMAIL = 'noreply@codango.com'

# Celery configuration
# The backend used to store task results using RabbitMQ as a broker
# This sends results back as AMQP messages
CELERY_RESULT_BACKEND = 'amqp'


# Scheduling periodic task with Celery
CELERYBEAT_SCHEDULE = {
    # Executes daily at midnight
    'popular-post-updates-daily': {
        'task': 'resources.tasks.send_recent_posts',
        'schedule': crontab(minute=0, hour=0),
        'args': ['daily'],
    },
    # Executes every sunday at midnight
    'popular-post-updates-weekly': {
        'task': 'resources.tasks.send_recent_posts',
        'schedule': crontab(minute=0, hour=0, day_of_week='sun'),
        'args': ['weekly'],
    },
    # Executes every first day of the month
    'popular-post-updates-monthly': {
        'task': 'resources.tasks.send_recent_posts',
        'schedule': crontab(0, 0, day_of_month='1'),
        'args': ['monthly'],
    },
}

# Celery Test Runner for unit tests
TEST_RUNNER = 'djcelery.contrib.test_runner.CeleryTestSuiteRunner'

TIME = 20
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = TIME    # change expired session
SESSION_IDLE_TIMEOUT = TIME  # logout
