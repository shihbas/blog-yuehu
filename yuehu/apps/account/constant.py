# coding=utf-8

ACCOUNT_REGISTER_TYPE_EMAIL = 0
ACCOUNT_REGISTER_TYPE_WEIBO = 1
ACCOUNT_REGISTER_TYPE_GITHUB = 2

PWD_MAX_LENGTH = 16
PWD_MIN_LENGTH = 8

EMAIL_CODE_CACHE_MAX = 60 * 10

GENDER_CHOICES = (
        (0, "女"),
        (1, "男"),

    )

CACHE_REGISTER_EMAIL_CODE = "REGISTER_EMAIL_CODE_{email_code}".format
CACHE_FORGOT_PWD_EMAIL_CODE = "FORGOT_PWD_EMAIL_CODE_{email_code}".format
CACHE_BIND_EMAIL_CODE = "CACHE_BIND_EMAIL_CODE_{email_code}".format
CACHE_ADMIN_LOGIN_PWD_EMAIL_CODE = "ADMIN_LOGIN_PWD_EMAIL_CODE_{email_code}".format



DEFAULT_AVATAR_URL = "https://img.python-dog.com/default/avatar/Samoyed_coding_120x120.jpeg"

NICKNAME_CHANGE_INTERVAL_DAY = 7
AVATAR_CHANGE_INTERVAL_DAY = 3
