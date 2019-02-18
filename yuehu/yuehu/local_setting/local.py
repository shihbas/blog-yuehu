# coding=utf-8
import os


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mysql',
        'PORT': '3306',
        'NAME': 'yuehu',
        'USER': 'root',
        'PASSWORD': 'root',
        'OPTIONS': {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
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

# 不使用默认缓存存储作为session存储
SESSION_ENGINE = 'redis_sessions.session'

# 配置session redis
SESSION_REDIS = {
    'host': 'redis_session',
    'port': 6379,
    'db': 0,
    'prefix': 'session',
    'socket_timeout': 2,
    'retry_on_timeout': False
    }


DEBUG = True


DOMAIN_NAME = "https://*********"

# oauth
# # weibo
WEIBO_CLINT_ID = os.environ.get("WEIBO_CLINT_ID")
WEIBO_CLINT_SECRET = os.environ.get("WEIBO_CLINT_SECRET")
WEIBO_SCOPE = ["all", "follow_app_official_microblog"]
WEIBO_REDIRECT_URI = f"{DOMAIN_NAME}/oauth/weibo"

# # github oauth
GITHUB_CLINT_ID = os.environ.get("GITHUB_CLINT_ID")
GITHUB_CLINT_SECRET = os.environ.get("GITHUB_CLINT_SECRET")
GITHUB_SCOPE = ["user"]
GITHUB_REDIRECT_URI = f"{DOMAIN_NAME}/oauth/github"

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = '*********@163.com'
EMAIL_HOST_PASSWORD = '*********'
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# SERVER_EMAIL = DEFAULT_FROM_EMAIL
#
# ADMINS = (
#     ('python_dog', 'python_dog@163.com'),
# )

## 管理员接受评论的邮箱列表
PYTHON_DOG_ADMIN_EMAIL_LIST = ['********@qq.com']


# rest framework
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
    'DEFAULT_VERSION': '1.0',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

REGISTER_URL = 'http://127.0.0.1:8080/check/register/email?code={code}'.format
RESET_PWD_URL = 'http://127.0.0.1:8080/check/reset/pwd?code={code}'.format
BIND_EMAIL_URL = 'http://127.0.0.1:8080/check/bind/email?code={code}'.format


# 消息队列配置
CELERY_BROKER_URL = 'redis://redis:6379/3'
