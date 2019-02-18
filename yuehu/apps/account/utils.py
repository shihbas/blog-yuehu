# coding=utf-8

from django.template import loader
from django.conf import settings
from django.utils import timezone

from account import constant as account_constant
from account.models import User

from common.function import send_email_format_html
from common.function import create_random_code
from common import constant as common_constant

from helper.logs import get_logger

logger = get_logger(__name__)


def create_account(username: str, password: str, register_type=account_constant.ACCOUNT_REGISTER_TYPE_EMAIL,
                   **extra_fields):
    """
        创建用户
    :param username: 用户名 str
    :param password: 密码 str
    :param register_type: 注册类型 int (默认为邮箱类型)
    :param extra_fields: 额外扩展字段
    :return: created, user
    """
    try:
        email = extra_fields.get("email", None)
        phone = extra_fields.get("phone", None)
        avatar = extra_fields.get("avatar", None)
        nickname = extra_fields.get("nickname", None)
        gender = extra_fields.get("gender")

        user = User()
        user.email = email
        user.phone = phone
        user.avatar = avatar
        user.nickname = nickname
        user.gender = gender

        user.username = username
        user.register_type = register_type
        user.set_password(password)

        # 初始化修改头像等时间为10天前，以便可以创建后直接修改头像等
        default_change_datetime = timezone.datetime.now().date() - timezone.timedelta(days=10)
        user.avatar_change_date = default_change_datetime
        user.nickname_change_date = default_change_datetime

        user.save()
        return True, user

    except Exception as e:
        logger.error(e)
        return False, None


def random_password(length=16):
    """
        创建随机密码
    :param length: 随机密码长度
    :return:
    """
    return create_random_code(length=length, mode=common_constant.MODE8)


def send_email_register(register_url_code, address_email):
    """
        发送注册验证邮件
    :param register_url_code: 注册code
    :param address_email: 邮件地址
    :return: 是否成功
    """

    register_url = settings.REGISTER_URL(code=register_url_code)

    tmp = loader.get_template("EmailRegister.html")
    msg = tmp.render({"register_url": register_url})
    return send_email_format_html("注册验证码", msg, [address_email])


def send_email_forgot_pwd(email_code, address_email):
    """
        发送忘记密码验证邮件
    :param email_code: 邮件验证码
    :param address_email: 邮件地址
    :return: 是否成功
    """

    forget_pwd_url = settings.RESET_PWD_URL(code=email_code)

    tmp = loader.get_template("EmailForgotPwd.html")
    msg = tmp.render({"forget_pwd_url": forget_pwd_url})
    return send_email_format_html("忘记密码", msg, [address_email])


def send_email_html_oauth_once_pwd(name, password, oauth_register, address_email):
    """
        第三方登录，有邮箱的情况下，新建用户的初始密码
    :param name:
    :param password:
    :param oauth_register:
    :param address_email:
    :return:
    """
    tmp = loader.get_template("EmailOauthRegister.html")
    msg = tmp.render({
        "name": name,
        "password": password,
        "oauth_register": oauth_register,
        "domain_name": settings.DOMAIN_NAME
    })

    return send_email_format_html("第三方登录提醒", msg, [address_email])


def send_email_html_oauth_old_account(name, oauth_register, address_email):
    """
        第三方登录，有邮箱的情况下，旧用户的连接
    :param name:
    :param oauth_register:
    :param address_email:
    :return:
    """
    tmp = loader.get_template("EmailOauthLink.html")
    msg = tmp.render({
        "name": name,
        "oauth_register": oauth_register,
        "domain_name": settings.DOMAIN_NAME
    })

    return send_email_format_html("第三方登录提醒", msg, [address_email])


def send_email_html_bind_email(email_code, nickname, address_email):
    """
        发送绑定邮箱的确认邮件
    :param email_code: 邮件验证码
    :param nickname: 用户昵称
    :param address_email: 地址
    :return: 是否成功
    """
    bind_email_url = settings.BIND_EMAIL_URL(code=email_code)
    tmp = loader.get_template("EmailBindEmail.html")
    msg = tmp.render({
        "name": nickname,
        "bind_email_url": bind_email_url
    })
    return send_email_format_html("绑定邮箱确认邮件", msg, [address_email])


def send_email_html_admin_login(email_code, address_email):
    """
        发送管理员登录验证邮件
    :param email_code:
    :param address_email:
    :return:
    """

    tmp = loader.get_template("EmailForgotPwd.html")
    msg = tmp.render({"email_code": email_code})
    return send_email_format_html("管理员登录验证", msg, [address_email])
