# coding=utf-8

from common.permissions.base import CMSBasePermission

from account.permissions import constant as ap_constant


class CMSSelfArticleManager(CMSBasePermission):

    has_one_perm_list = [f"account.{ap_constant.CMS_MANAGE_ALL_ARTICLE}",
                         f"account.{ap_constant.CMS_MANAGE_SELF_ARTICLE}"]


class CMSAllArticleManager(CMSBasePermission):

    has_one_perm_list = [f"account.{ap_constant.CMS_MANAGE_ALL_ARTICLE}"]


class CMSAllTagManager(CMSBasePermission):

    has_one_perm_list = [f"account.{ap_constant.CMS_MANAGE_ARTICLE_TAGS}"]

