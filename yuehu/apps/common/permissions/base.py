# coding=utf-8

from account.permissions import constant as ap_constant


class CMSBasePermission(object):

    has_all_perm_list = []

    has_one_perm_list = []

    def has_permission(self, request, view):

        if not request.user.is_authenticated or not request.user.has_perm(f"account.{ap_constant.CAN_LOGIN_CMS}"):
            return False

        return request.user.is_superuser or \
            self.check_perm_list_has_one(request) or \
            self.check_perm_list_has_all(request)

    def has_object_permission(self, request, view, obj):
        """
            Return `True` if permission is granted, `False` otherwise.
        :param request:
        :param view:
        :param obj:
        :return:
        """
        return True

    def check_perm_list_has_one(self, request):
        """
            校验单独权限是否有权限符合
        :param request:
        :return:
        """
        for perm in self.has_one_perm_list:
            if request.user.has_perm(perm):
                return True

        return False

    def check_perm_list_has_all(self, request):
        """

        :param request:
        :return:
        """

        return all([request.user.has_perm(perm) for perm in self.has_all_perm_list])

