# coding=utf-8

from django.core.cache import cache

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from account.models import User, UserDefaultAvatar
from account import constant as account_constant
from account.utils import send_email_html_bind_email
from account.serializers.api import ApiUserDefaultAvatarSerializer

from common.permissions import IsLogin
from common.decorators import api_common, common_validate
from common import constant as common_constant
from common.function import email_rightful, create_random_code
from common.exceptions import LogicException


class UserInfoApi(APIView):

    permission_classes = (IsLogin,)

    required_fields1 = ['pwd1', 'pwd2']

    type_fields1 = {
        'pwd1': str,
        'pwd2': str
    }
    logic_filed1 = {
        'pwd1': (lambda x: account_constant.PWD_MIN_LENGTH < len(x) < account_constant.PWD_MAX_LENGTH,
                     f"密码长度应大于{account_constant.PWD_MIN_LENGTH}位，小于{account_constant.PWD_MAX_LENGTH}")
    }

    required_fields2 = ['nickname']

    type_fields2 = {
        'nickname': str
    }
    logic_filed2 = {
        'nickname': (lambda x: 1 < len(x) < 12, "昵称长度应在12个字内")
    }

    @api_common
    def get(self, request):
        """
            获取用户信息
        :param request:
        :return:
        """
        user = request.user
        return Response(data=user.display_user_info)

    @api_common
    @common_validate(required_fields=required_fields1, type_fields=type_fields1, logic_fields=logic_filed1)
    def post(self, request):
        """
            修改密码
        :param request:
        :return:
        """
        user = request.user
        password1 = request.data.get("pwd1")
        password2 = request.data.get("pwd2")
        if password1 != password2:
            raise LogicException("两次密码不一致")
        return Response(data=user.change_pwd(password1))

    @api_common
    @common_validate(required_fields=required_fields2, type_fields=type_fields2, logic_fields=logic_filed2)
    def put(self, request):
        """
            修改昵称
        :param request:
        :return:
        """
        user = request.user
        nickname = request.data.get("nickname")
        return Response(data={"updated": user.change_nickname(nickname=nickname)})


class DefaultAvatarApi(APIView):
    """
        默认头像
    """

    permission_classes = (IsLogin,)

    required_fields = ['code']

    type_fields = {
        'code': str
    }

    @api_common
    def get(self, request):
        data_ser = ApiUserDefaultAvatarSerializer(UserDefaultAvatar.objects.all()[:20], many=True)
        return Response(data=data_ser.data)

    @api_common
    @common_validate(required_fields=required_fields, type_fields=type_fields)
    def put(self, request):
        user = request.user
        code = request.data.get("code")
        return Response(data={"updated": user.change_default_avatar(code)})


class BindEmailApi(APIView):

    permission_classes = (IsLogin,)

    required_fields = ['email']

    type_fields = {
        'email': str
    }

    @api_common
    @common_validate(required_fields=required_fields, type_fields=type_fields)
    def post(self, request):
        user = request.user
        email = request.data.get("email")

        if user.email:
            raise LogicException("绑定失败:用户已经绑定了邮箱")

        right, email = email_rightful(email)
        if not right:
            raise LogicException("绑定失败:邮箱格式不正确")

        if User.objects.filter(email=email).exists():
            raise LogicException("绑定失败:邮箱已经被注册或绑定了")

        email_code = create_random_code(length=12, mode=common_constant.MODE5)

        if send_email_html_bind_email(email_code, user.display_name, email):
            cache.set(
                    account_constant.CACHE_BIND_EMAIL_CODE(email_code=email_code),
                    {
                        "email": email,
                        "open_id": user.open_id
                    },
                    account_constant.EMAIL_CODE_CACHE_MAX
                )
        else:
            raise LogicException("发送邮件失败:请检查邮箱或联系我！")

        return Response({"bind": "success"})


check_self_bind_email_required_fields = ['code']

check_self_bind_email_type_fields = {
    'code': str
}
@api_view(["PUT"])
@api_common
@common_validate(required_fields=check_self_bind_email_required_fields, type_fields=check_self_bind_email_type_fields)
def check_self_bind_email(request):
    email_code = request.data.get("code", None)

    user_info = cache.get(account_constant.CACHE_BIND_EMAIL_CODE(email_code=email_code), None)

    if not user_info:
        return Response({"text": "邮箱链接失效", "success": 0})

    if not isinstance(user_info, dict):
        return Response({"text": "邮箱链接有问题", "success": 0})

    email = user_info.get("email")
    open_id = user_info.get("open_id")

    user = User.objects.filter(oid=open_id).first()
    if user is None:
        return Response({"text": "找不到要绑定的用户", "success": 0})

    return Response({"text": f"账号已经成功绑定{user.bind_email(email)}", "success": 1})
