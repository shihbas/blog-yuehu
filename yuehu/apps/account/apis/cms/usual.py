# coding=utf-8

from django.core.cache import cache
from django.contrib.auth import login, authenticate, logout

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from common.permissions import IsNotLogin, IsLogin

from account.models import User
from account import constant as account_constant
from account.utils import send_email_html_admin_login
from account.permissions.cms import IsAdmin

from common.decorators import cms_common
from common import constant as common_constant
from common.function import email_rightful, create_random_code
from common.exceptions import ValidateException, LogicException


class CMSAdminLogin(APIView):

    permission_classes = (IsNotLogin,)

    @cms_common
    def put(self, request):
        """
            发送admin登录验证码
        :param request:
        :return:
        """

        email = request.data.get("email", None)

        ve = ValidateException()

        right, email = email_rightful(email)
        if not right:
            ve.add_message("email", "except")

        if ve.is_error():
            raise ve

        if not User.objects.filter(username=email, is_superuser=True).exists():
            raise LogicException("Em....")

        email_code = create_random_code(mode=common_constant.MODE5)
        if send_email_html_admin_login(email_code, email):
            email_code = email_code.lower()
            cache.set(
                account_constant.CACHE_ADMIN_LOGIN_PWD_EMAIL_CODE(email=email),
                email_code,
                account_constant.EMAIL_CODE_CACHE_MAX
            )
            return Response({"send": "success"})
        else:
            return Response({"send": "failure"})

    @cms_common
    def post(self, request):
        """
            admin登录(暂无验证)
        :param request:
        :return:
        """
        username = request.data.get("username", None)
        password = request.data.get("password", None)

        ve = ValidateException()
        if not password:
            ve.add_message("password1", "null")

        right, email = email_rightful(username)
        if not right:
            ve.add_message("email", "except")

        if ve.is_error():
            raise ve

        if not User.objects.filter(username=email).exists():
            raise LogicException("你走！你不是主人！")

        user = authenticate(request, username=email, password=password)

        if user is None:
            raise LogicException("登录失败，请检查账号密码是否正确")

        login(request, user)
        return Response({"login": "success", "token": user.open_id})


@api_view(["GET"])
@permission_classes((IsAdmin,))
@cms_common
def get_admin_info(request):
    """
        获取管理员的信息
    :param request:
    :return:
    """

    user = request.user

    return Response(data=user.display_admin_info)


@api_view(("GET",))
@permission_classes((IsLogin,))
@cms_common
def admin_logout(request):
    logout(request)
    return Response({"logout": "success"})
