"""
Django settings for yuehu project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys
import logging

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPS_DIR = os.path.join(BASE_DIR, "apps")
LOG_DIR = os.path.join(BASE_DIR, "logs")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

sys.path.insert(0, APPS_DIR)



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'j_2!7)--p6_gpq7k9cj#e@brvtqh4jlz$wmup2gx@o(4tbo@0c'

# SECURITY WARNING: don't run with debug turned on in production!`
DEBUG = False

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "rest_framework",
    "django_filters",

]

PROJECT_APPS = [
    "base",
    "common",
    "helper",

    "account",
    "banner",
    "article",
    "timeline",
    "photowall",

]

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'common.middleware.UserVisitMiddleware',
]

ROOT_URLCONF = 'yuehu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'yuehu.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_HTTPONLY = True

SESSION_COOKIE_AGE = 604800 * 8

CSRF_COOKIE_AGE = 604800 * 8

CSRF_COOKIE_HTTPONLY = False

LANGUAGE_CODE = 'zh_hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = False

USE_L10N = False

USE_TZ = True

AUTH_USER_MODEL = "account.User"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s'
        },
        'visit_article': {
            'format': '%(asctime)s|%(message)s'
        }
    },
    'filters': {
        'exclude_yuehu_action': {
            '()': 'helper.logs.ExcludeFilter',
            'exclude_name': 'yuehu.actions',
            'exclude_level': logging.ERROR
        },
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'all.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 0,
            'encoding': 'utf8',
            'formatter': 'standard',
        },
        'errors': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 0,
            'encoding': 'utf8',
            'formatter': 'standard',
        },
        'apps': {
            'level': 'INFO',
            'filters': ['exclude_yuehu_action'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'apps.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 0,
            'encoding': 'utf8',
            'formatter': 'standard',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'request_handler': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'script.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 0,
            'formatter': 'standard',
        },
        'action': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'action.log'),
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 0,
            'encoding': 'utf8',
            'formatter': 'standard',
        },
        'visit_article': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'visit_article.log'),
            'maxBytes': 1024 * 1024 * 5,  # 50 MB
            'backupCount': 0,
            'encoding': 'utf8',
            'formatter': 'visit_article',
        },
    },
    'loggers': {
        'yuehu': {
            'handlers': ['apps', 'errors'],
            'level': 'DEBUG',
            'propagate': True
        },
        'yuehu.actions': {
            'handlers': ['action', 'errors'],
            'level': 'DEBUG',
            'propagate': True
        },
        'django.request': {
            'handlers': ['request_handler'],
            'level': 'ERROR',
            'propagate': False,
        },
        'visit_article': {
            'handlers': ['visit_article'],
            'level': 'INFO',
            'propagate': True
        }
    }
}

# 消息队列 celery
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_COMPRESSION = 'gzip'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_REDIS_MAX_CONNECTIONS = 10
CELERY_ENABLE_UTC = False
CELERY_TIMEZONE = 'Asia/Shanghai'


DJANGO_LOCAL_SETTING = os.environ.get('DJANGO_LOCAL_SETTING', 'local')
exec('from yuehu.local_setting.{env} import *'.format(env=DJANGO_LOCAL_SETTING))
