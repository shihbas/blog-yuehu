# coding=utf-8

from common.permissions.base import CMSBasePermission

from account.permissions import constant as ap_constant


class IsAdmin(CMSBasePermission):
    pass


class CMSPermissionManager(CMSBasePermission):
    has_one_perm_list = [f"account.{ap_constant.CMS_MANAGE_PERMISSIONS}"]


class CMSAccountManager(CMSBasePermission):
    has_one_perm_list = [f"account.{ap_constant.CMS_MANAGE_ACCOUNTS}"]