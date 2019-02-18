# coding=utf-8

from django.conf.urls import url

from account.apis import apis, ouath, user
from account.apis.cms import usual, permission



api_urlpatterns = [
    url("^api/info/$", apis.user_info, name="user_info"),
    url("^api/email_register/$", apis.EmailRegister.as_view(), name="email_register"),
    url("^api/web_login/$", apis.web_login, name="web_login"),
    url("^api/web_logout/$", apis.web_logout, name="web_logout"),
    url("^api/email_forgot_password/$", apis.EmailForgotPassword.as_view(), name="email_forgot_password"),
    url("^api/change_password/$", apis.change_password, name="change_password"),
]

user_urlpatterns = [
    url("^api/user/info/base/$", user.UserInfoApi.as_view(), name="api_user_info"),
    url("^api/user/default/avatar/$", user.DefaultAvatarApi.as_view(), name="api_default_avatar"),
    url("api/user/bind/email/info/$", user.BindEmailApi.as_view(), name="api_bind_email"),
    url("api/user/bind/email/check/$", user.check_self_bind_email, name="api_check_self_bind_email")
]

oauth_urlpatterns = [
    url("^oauth/weibo_login/$", ouath.WeiBoLogin.as_view(), name="weibo_login"),
    url("^oauth/github_login/$", ouath.GitHubLogin.as_view(), name="github_login"),
]

cms_urlpatterns = [
    url("^cms/login/$", usual.CMSAdminLogin.as_view(), name="cms_login"),
    url("^cms/admin_info/$", usual.get_admin_info, name="cms_admin_info"),
    url("^cms/logout/$", usual.admin_logout, name="admin_logout"),
    # permission
    url("^cms/permission/manage/group/$", permission.CMSManagePermissionGroup.as_view(), name='cms_manage_group'),
    url("^cms/permission/manage/permission_by_group/$", permission.CMSManagePermissionByGroup.as_view(), name="cms_manage_permission_by_group"),
    url("^cms/permission/manage/account_by_group/$", permission.CMSManageAccountByGroup.as_view(), name='cms_manage_account_by_group'),
    url("^cms/permission/get_all_account_permissions/$", permission.get_all_account_permissions, name="cms_get_all_account_permissions"),
    url("^cms/permission/get_all_account_permission_groups/$", permission.get_all_account_permission_groups, name="cms_get_all_account_permission_groups"),
    url("^cms/permission/get_account_detail_by_username/$", permission.get_account_detail_by_username, name="cms_get_account_detail_by_username")
]

urlpatterns = api_urlpatterns + oauth_urlpatterns + cms_urlpatterns + user_urlpatterns
