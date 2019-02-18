# coding=utf-8
import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mysql',
        'PORT': '3306',
        'NAME': 'yuehu',
        'USER': 'root',
        'PASSWORD': '*******',
        'OPTIONS': {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4'
        }
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://:@redis:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cache'

DEBUG = True

DOMAIN_NAME = "https://web.shihbas.cn"

# oauth
# # weibo
WEIBO_CLINT_ID = os.environ.get("WEIBO_CLINT_ID")
WEIBO_CLINT_SECRET = os.environ.get("WEIBO_CLINT_SECRET")
WEIBO_SCOPE = ["all", "follow_app_official_microblog"]
WEIBO_REDIRECT_URI = "{domain_name}/oauth/weibo".format(domain_name=DOMAIN_NAME)

# # github oauth
GITHUB_CLINT_ID = os.environ.get("GITHUB_CLINT_ID")
GITHUB_CLINT_SECRET = os.environ.get("GITHUB_CLINT_SECRET")
GITHUB_SCOPE = ["user"]
GITHUB_REDIRECT_URI = "{domain_name}/oauth/github".format(domain_name=DOMAIN_NAME)

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = '********@163.com'
EMAIL_HOST_PASSWORD = '*********'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

## 管理员接受评论的邮箱列表
PYTHON_DOG_ADMIN_EMAIL_LIST = ['*********@qq.com']


# rest framework
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
    'DEFAULT_VERSION': '1.0',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

REGISTER_URL = 'https://web.shihbas.cn/check/register/email?code={code}'.format
RESET_PWD_URL = 'https://web.shihbas.cn/check/reset/pwd?code={code}'.format
BIND_EMAIL_URL = 'https://web.shihbas.cn/check/bind/email?code={code}'.format

# 消息队列配置
CELERY_BROKER_URL = 'redis://redis:6379/3'
