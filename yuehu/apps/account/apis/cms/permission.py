# coding=utf-8

from django.contrib.auth.models import Permission, Group
from django.db import transaction

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from common.decorators import cms_common, common_validate
from common.exceptions import LogicException

from account.models import User
from account import constant as account_constant
from account.permissions.cms import CMSPermissionManager
from account.serializers.cms import CMSGroupDetailSerializer, CMSAccountListForGroup, CMSAccountDetailForGroup, \
    CMSGroupListSerializer

from helper.logs import get_logger

logger = get_logger(__name__)


class CMSManagePermissionGroup(APIView):
    """ 管理权限组 """

    permission_classes = (CMSPermissionManager,)

    required_fields1 = ['name']

    required_fields2 = ['old_name', 'new_name']

    @cms_common
    def get(self, request):
        groups = Group.objects.prefetch_related("permissions").all()
        group_ser = CMSGroupDetailSerializer(groups, many=True)

        return Response(data=group_ser.data)

    @cms_common
    @common_validate(required_fields=required_fields1)
    def post(self, request):
        name = request.data.get("name")

        group, created = Group.objects.get_or_create(name=name)

        return Response({"created": created})

    @cms_common
    @common_validate(required_fields=required_fields2)
    def put(self, request):
        old_name = request.data.get("old_name")
        new_name = request.data.get("new_name")

        if Group.objects.filter(name=new_name).exists():
            raise LogicException("已有该名称的组了！")

        updated = Group.objects.filter(name=old_name).update(
            name=new_name
        )

        return Response({"updated": updated})

    @cms_common
    def delete(self, request):
        name = request.GET.get("name")
        group = Group.objects.filter(name=name).first()

        if group is None:
            raise LogicException(f"名称为{name}的权限组找不到")
        try:
            deleted = True
            with transaction.atomic():
                # 清理与权限的关系
                group.permissions.clear()
                # 清理与用户的关系
                group.user_set.clear()
                # 删除组
                group.delete()
        except Exception as e:
            logger.error(e)
            deleted = False

        return Response({"deleted": deleted})


class CMSManagePermissionByGroup(APIView):
    """ 管理权限组内的权限 """
    permission_classes = (CMSPermissionManager,)

    required_fields = ['name']

    logic_fields = {
        "permission_list": (lambda x: isinstance(x, list), "permission_list 应该为 list")
    }

    @cms_common
    @common_validate(required_fields=required_fields, logic_fields=logic_fields)
    def put(self, request):
        name = request.data.get("name")
        permission_list = request.data.get("permission_list")

        group = Group.objects.filter(name=name).first()

        if group is None:
            raise LogicException(f"名称为{name}的权限组找不到")

        permissions = Permission.objects.filter(codename__in=permission_list)

        if permissions:
            group.permissions.set(permissions)
        else:
            group.permissions.clear()

        return Response({"updated": True})


@api_view(["GET"])
@permission_classes((CMSPermissionManager,))
@cms_common
def get_all_account_permissions(request):
    """
        获取所有权限
    :param request:
    :return:
    """
    return Response(data=User.get_all_permission_dict())


@api_view(["GET"])
@permission_classes((CMSPermissionManager,))
@cms_common
def get_all_account_permission_groups(request):
    """
        获取所有权限组
    :param request:
    :return:
    """
    groups = Group.objects.all()
    groups_ser = CMSGroupListSerializer(groups, many=True)
    return Response(data=groups_ser.data)



class CMSManageAccountByGroup(APIView):
    """ 管理账户所在的权限组 """

    permission_classes = (CMSPermissionManager,)

    required_fields1 = ['open_id']

    required_fields2 = ['open_id']

    logic_filed2 = {
        "group_list": (lambda x: isinstance(x, list), "group_list 应该为 list")
    }

    @cms_common
    def get(self, request):
        users = User.objects.prefetch_related('groups').filter(is_cms=True)
        users_ser = CMSAccountListForGroup(users, many=True)

        return Response(data=users_ser.data)

    @cms_common
    @common_validate(required_fields=required_fields1)
    def post(self, request):
        open_id = request.data.get("open_id")
        updated = User.objects.filter(oid=open_id).update(
            is_cms=True
        )

        return Response({"created": updated})

    @cms_common
    @common_validate(required_fields=required_fields2, logic_fields=logic_filed2)
    def put(self, request):
        open_id = request.data.get("open_id")
        group_list = request.data.get("group_list")

        account = User.objects.filter(oid=open_id).first()

        if account is None:
            raise LogicException(f"没有open_id为{open_id} 的账号")

        groups = Group.objects.filter(name__in=group_list)
        if group_list:
            account.groups.set(groups)
        else:
            account.groups.clear()

        return Response({"updated": True})

    @cms_common
    @common_validate(required_fields=required_fields2)
    def delete(self, request):
        open_id = request.GET.get("open_id")

        account = User.objects.filter(oid=open_id).first()
        if account is None:
            raise LogicException(f"没有open_id为{open_id} 的账号")

        try:
            deleted = True
            with transaction.atomic():
                account.groups.clear()
                account.is_cms = False
                account.save()
        except Exception as e:
            logger.error(e)
            deleted = False

        return Response({"deleted": deleted})


@api_view(["GET"])
@permission_classes((CMSPermissionManager,))
@cms_common
def get_account_detail_by_username(request):
    """
        通过用户名找到账户
    :param request:
    :return:
    """
    username = request.GET.get("username")
    account = User.objects.filter(username=username).first()
    if account is None:
        raise LogicException(f"用户名{username}无效")
    account_ser = CMSAccountDetailForGroup(account)
    return Response(data=account_ser.data)
