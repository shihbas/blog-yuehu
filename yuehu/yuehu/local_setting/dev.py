# coding=utf-8
import os

MYSQL_HOST = os.environ.get("YUEHU_MYSQL_HOST", "mysql")
MYSQL_PROT = os.environ.get("YUEHU_MYSQL_PORT", '3306')
MYSQL_USER = os.environ.get("YUEHU_MYSQL_USER", "root")
MYSQL_PWD = os.environ.get("YUEHU_MYSQL_PWD", "")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': MYSQL_HOST,
        'PORT': MYSQL_PROT,
        'NAME': 'yuehu',
        'USER': MYSQL_USER,
        'PASSWORD': MYSQL_PWD,
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


DEBUG = False

DOMAIN_NAME = "https://www.python-dog.com"

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


YUEHU_EMAIL_PWD = os.environ.get("YUEHU_EMAIL_PWD", "")
# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.163.com"
EMAIL_PORT = 465
EMAIL_HOST_USER = 'python_dog@163.com'
EMAIL_HOST_PASSWORD = YUEHU_EMAIL_PWD
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

## 管理员接受评论的邮箱列表
PYTHON_DOG_ADMIN_EMAIL_LIST = ['python_dog@163.com']


# rest framework
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.QueryParameterVersioning',
    'DEFAULT_VERSION': '1.0',
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
}

REGISTER_URL = 'https://www.python-dog.com/check/register/email?code={code}'.format
RESET_PWD_URL = 'https://www.python-dog.com/check/reset/pwd?code={code}'.format
BIND_EMAIL_URL = 'https://www.python-dog.com/check/bind/email?code={code}'.format

# 消息队列配置
CELERY_BROKER_URL = 'redis://redis:6379/3'
