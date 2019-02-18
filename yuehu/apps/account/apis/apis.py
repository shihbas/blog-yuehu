# coding=utf-8

from django.core.cache import cache
from django.contrib.auth import login, logout, authenticate

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from common.permissions import IsNotLogin, IsLogin
from account.models import User
from account import constant as account_constant
from account.utils import create_account, send_email_forgot_pwd, send_email_register

from common.decorators import api_common
from common import constant as common_constant
from common.function import email_rightful, create_random_code
from common.exceptions import ValidateException, LogicException


class EmailRegister(APIView):

    permission_classes = (IsNotLogin,)

    @api_common
    def post(self, request):
        email = request.data.get("email", None)
        password1 = request.data.get("password1")
        password2 = request.data.get("password2")

        if account_constant.PWD_MIN_LENGTH > len(password1) or account_constant.PWD_MAX_LENGTH < len(password1):
            raise LogicException(f"密码长度应大于{account_constant.PWD_MIN_LENGTH}位，小于{account_constant.PWD_MAX_LENGTH}")

        right, email = email_rightful(email)
        if not right:
            raise LogicException("邮箱格式不正确")

        if User.objects.filter(username=email).exists():
            raise LogicException("邮箱已经注册了")

        if password1 != password2:
            raise LogicException("两次密码不一致")

        email_code = create_random_code(length=12, mode=common_constant.MODE5)
        if send_email_register(email_code, email):
            cache.set(
                    account_constant.CACHE_REGISTER_EMAIL_CODE(email_code=email_code),
                    {
                        "email": email,
                        "password": password1
                    },
                    account_constant.EMAIL_CODE_CACHE_MAX
                )
        else:
            raise LogicException("发送失败！请检查邮箱或联系我！")

        return Response({"register": "success"})

    @api_common
    def put(self, request):
        code = request.data.get("code", None)

        user_info = cache.get(account_constant.CACHE_REGISTER_EMAIL_CODE(email_code=code), None)

        if not user_info:
            return Response({"text": "邮箱链接失效", "success": 0})

        if not isinstance(user_info, dict):
            return Response({"text": "邮箱链接有问题", "success": 0})

        email = user_info.get("email")
        pwd = user_info.get("password")

        if User.objects.filter(username=email).exists():
            return Response({"text": "创建成功", "success": 1})


        created, user = create_account(
            username=email,
            password=pwd,
            register_type=account_constant.ACCOUNT_REGISTER_TYPE_EMAIL,
            email=email
        )

        if not created:
            return Response({"text": "创建用户失败", "success": 0})

        return Response({"text": "创建成功", "success": 1})


@api_view(("POST",))
@api_common
def web_login(request):
    username = request.data.get("username", None)
    password = request.data.get("password", None)

    if request.user.is_authenticated:
        raise LogicException("你已经登录了")

    ve = ValidateException()
    if not username:
        ve.add_message("username", "null")
    if not password:
        ve.add_message("password", "null")

    if ve.is_error():
        raise ve

    user = authenticate(request, username=username, password=password)

    if user is None:
        raise LogicException("登录失败，请检查账号密码是否正确")

    login(request, user)
    return Response(user.display_info)


@api_view(("GET",))
@api_common
def web_logout(request):

    if not request.user.is_authenticated:
        raise LogicException("你已经退出登录了")

    logout(request)
    return Response({"logout": "success"})


class EmailForgotPassword(APIView):

    permission_classes = (IsNotLogin,)

    @api_common
    def post(self, request):
        email = request.data.get("email", None)
        password1 = request.data.get("password1")
        password2 = request.data.get("password2")

        if account_constant.PWD_MIN_LENGTH > len(password1) or account_constant.PWD_MAX_LENGTH < len(password1):
            raise LogicException(f"密码长度应大于{account_constant.PWD_MIN_LENGTH}位，小于{account_constant.PWD_MAX_LENGTH}")

        right, email = email_rightful(email)
        if not right:
            raise LogicException("邮箱格式不正确")

        if not User.objects.filter(username=email).exists():
            raise LogicException("邮箱未注册！")

        if password1 != password2:
            raise LogicException("两次密码不一致")

        email_code = create_random_code(length=12, mode=common_constant.MODE5)
        if send_email_forgot_pwd(email_code, email):
            cache.set(
                    account_constant.CACHE_FORGOT_PWD_EMAIL_CODE(email_code=email_code),
                    {
                        "email": email,
                        "password": password1
                    },
                    account_constant.EMAIL_CODE_CACHE_MAX
                )
        else:
            raise LogicException("发送失败！请检查邮箱或联系我！")

        return Response({"register": "success"})

    @api_common
    def put(self, request):
        email_code = request.data.get("code", None)

        user_info = cache.get(account_constant.CACHE_FORGOT_PWD_EMAIL_CODE(email_code=email_code), None)

        if not user_info:
            return Response({"text": "邮箱链接失效", "success": 0})

        if not isinstance(user_info, dict):
            return Response({"text": "邮箱链接有问题", "success": 0})

        email = user_info.get("email")
        pwd = user_info.get("password")

        user = User.objects.filter(username=email).first()
        if user is None:
            return Response({"text": "该邮箱没有注册过不能重置密码", "success": 0})

        if user.change_pwd(pwd):
            return Response({"text": "重置成功", "success": 1})

        return Response({"text": "重置密码失败，请联系我！", "success": 0})


@api_view(("POST",))
@permission_classes((IsLogin,))
@api_common
def change_password(request):
    password1 = request.data.get("password1")
    password2 = request.data.get("password2")

    ve = ValidateException()
    if not password1:
        ve.add_message("password1", "null")
    if not password2:
        ve.add_message("password2", "null")

    if account_constant.PWD_MIN_LENGTH > len(password1) or account_constant.PWD_MAX_LENGTH < len(password1):
        ve.add_message("password1", "except")

    if account_constant.PWD_MIN_LENGTH > len(password2) or account_constant.PWD_MAX_LENGTH < len(password2):
        ve.add_message("password2", "except")

    if password1 != password2:
        raise LogicException("两次密码不一致")

    user = request.user
    if user.change_pwd(password1):
        return Response({"change": "success"})
    else:
        raise LogicException("服务错误请重新提交")


@api_view(("GET",))
@permission_classes((IsLogin,))
@api_common
def user_info(request):
    user = request.user
    return Response(user.display_info)
