# coding=utf-8

from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from account.mixin import OpenIdMixin
from account.managers import UserManager
from account import constant as account_constant
from account.permissions import constant as ap_constant

from base.models import BaseDeleteModel

from common.mixin import OpenCodeMixin
from common.exceptions import LogicException
from common.function import fuzzy_real_email

from helper.logs import get_logger

logger = get_logger(__name__)


class User(AbstractBaseUser, PermissionsMixin, OpenIdMixin):

    username = models.CharField(
        max_length=128,
        unique=True
    )

    phone = models.CharField(
        max_length=32,
        unique=True,
        null=True,
        blank=True,
    )

    email = models.CharField(
        max_length=48,
        unique=True,
        null=True,
        blank=True
    )

    nickname = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )
    nickname_change_date = models.DateField(
        default=timezone.now
    )

    remark_name = models.CharField(
        max_length=16,
        blank=True,
        null=True
    )

    avatar = models.URLField(
        max_length=256,
        blank=True,
        null=True
    )

    avatar_change_date = models.DateField(
        default=timezone.now
    )

    gender = models.PositiveSmallIntegerField(
        choices=account_constant.GENDER_CHOICES,
        null=True,
        blank=True,
    )

    is_staff = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    # 能够在后台赋予权限时可见
    is_cms = models.BooleanField(
        default=False
    )

    date_joined = models.DateTimeField(
        auto_now_add=True
    )

    register_type = models.PositiveSmallIntegerField(
        default=account_constant.ACCOUNT_REGISTER_TYPE_EMAIL
    )

    @property
    def display_name(self):
        return self.nickname or self.display_email or self.display_username

    @property
    def display_username(self):
        """
            展示的用户名
        :return:
        """
        return self.username[0:5] + "*"*4 + self.username[:3]


    @property
    def display_phone(self):
        if self.phone is None:
            return ""

        return self.phone[:3] + "*"*4 + self.phone[-4:]

    @property
    def display_email(self):
        if self.email is None:
            return ""
        else:
            return fuzzy_real_email(self.email)

    @property
    def display_avatar(self):
        return self.avatar or account_constant.DEFAULT_AVATAR_URL

    @property
    def display_info(self):
        info_data = dict()
        info_data["display_name"] = self.display_name
        # info_data["phone"] = self.display_phone
        # info_data["email"] = self.display_email
        info_data["avatar"] = self.display_avatar
        info_data["open_id"] = self.open_id
        return info_data

    @property
    def display_admin_info(self):
        info_data = dict()
        info_data["nickname"] = self.display_name
        info_data["avatar"] = self.display_avatar
        info_data["perm_list"] = self.get_all_permissions()
        return info_data

    @property
    def display_user_info(self):
        now_date = timezone.datetime.now().date()
        nickname_interval_date = now_date - self.nickname_change_date
        avatar_interval_date = now_date - self.avatar_change_date

        info_data = dict()
        info_data["avatar"] = self.display_avatar
        info_data["avatar_interval_days"] = avatar_interval_date.days
        info_data["nickname"] = self.display_name
        info_data["nickname_interval_days"] = nickname_interval_date.days
        info_data["email"] = self.display_email
        info_data["open_id"] = self.open_id
        return info_data


    @classmethod
    def get_all_permission_list(cls):
        """
            获取Account所有的权限 列表
        :return:
        """
        return [item[0] for item in cls._meta.permissions]

    @classmethod
    def get_all_permission_dict(cls):
        """
            获取Account所有的权限 字典
        :return:
        """
        return [{'codename': item[0], 'name': item[1]} for item in cls._meta.permissions]

    def change_pwd(self, password):
        """
            修改用户密码
        :param password:
        :return:
        """
        try:
            self.set_password(password)
            self.save()
            return 1
        except Exception as e:
            logger.error(e)
            raise LogicException(f'修改失败:未知错误修改失败')

    def change_nickname(self, nickname):
        """
            修改昵称
        :param nickname:
        :return:
        """
        now_date = timezone.datetime.now().date()
        interval_date = now_date - self.nickname_change_date
        if account_constant.NICKNAME_CHANGE_INTERVAL_DAY > interval_date.days:
            raise LogicException(f'修改失败:在最近的{account_constant.NICKNAME_CHANGE_INTERVAL_DAY}天内你修改过了昵称，现在不能修改了')
        if User.objects.filter(nickname=nickname).exists():
            raise LogicException(f'修改失败:昵称{nickname}已经存在了！请更换一个')
        self.nickname = nickname
        self.nickname_change_date = now_date
        self.save()
        return 1

    def change_default_avatar(self, avatar_code):
        """
            挑选默认头像替换原头像
        :param avatar_code:
        :return:
        """
        now_date = timezone.datetime.now().date()
        interval_date = now_date - self.avatar_change_date
        if account_constant.AVATAR_CHANGE_INTERVAL_DAY > interval_date.days:
            raise LogicException(f'修改失败:在最近的{account_constant.AVATAR_CHANGE_INTERVAL_DAY}天内你修改过了头像，现在不能修改了')

        avatar = UserDefaultAvatar.objects.filter(open_code=avatar_code).first()
        if avatar is None:
            raise LogicException(f'修改失败:你所选的头像不是python-dog提供的默认头像集内的')
        self.avatar = avatar.avatar_url
        self.avatar_change_date = now_date
        self.save()
        return 1

    def bind_email(self, email):
        """
            绑定邮箱
        :param email:
        :return:
        """
        if self.email:
            return self.email

        self.email = email
        self.save()
        return email



    USERNAME_FIELD = "username"

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        swappable = "AUTH_USER_MODEL"

        permissions = (
            # usual
            (ap_constant.CAN_LOGIN_CMS, "能登录CMS"),
            # dashboard
            (ap_constant.CMS_MANAGE_DASHBOARD, "CMS-管理数据"),
            # article
            (ap_constant.CMS_MANAGE_SELF_ARTICLE, "CMS-管理自己的文章"),
            (ap_constant.CMS_MANAGE_ALL_ARTICLE, "CMS-管理全部的文章"),
            ## tag
            (ap_constant.CMS_MANAGE_ARTICLE_TAGS, "CMS-管理所有标签"),
            # photo wall
            (ap_constant.CMS_MANAGE_PHOTO_WALL, "CMS-管理图片墙"),
            # timeline
            (ap_constant.CMS_MANAGE_TIMELINE, "CMS-管理时间线"),
            # banner
            ## slide show
            (ap_constant.CMS_MANAGE_BANNER_SLIDE_SHOW, "CMS-管理横幅-首页轮播"),
            # permission
            (ap_constant.CMS_MANAGE_PERMISSIONS, "CMS-管理用户权限"),
            # account
            (ap_constant.CMS_MANAGE_ACCOUNTS, "CMS-管理所有账号")
        )


class WeiBoUser(models.Model):
    uid = models.CharField(
        max_length=32,
        unique=True,
    )

    name = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )

    avatar = models.URLField(
        max_length=1024,
        blank=True,
        null=True
    )

    gender = models.PositiveSmallIntegerField(
        choices=account_constant.GENDER_CHOICES,
        null=True,
        blank=True,
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )

    last_update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="最后更新时间"
    )

    user = models.OneToOneField(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )


class GitHubUser(models.Model):

    uid = models.CharField(
        max_length=32,
        unique=True,
    )

    name = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )

    avatar = models.URLField(
        max_length=1024,
        blank=True,
        null=True
    )

    email = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )

    last_update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="最后更新时间"
    )

    user = models.OneToOneField(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.PROTECT
    )


class UserDefaultAvatar(BaseDeleteModel, OpenCodeMixin):
    avatar_url = models.CharField(
        max_length=256
    )
    sort_id = models.PositiveSmallIntegerField(default=0)
