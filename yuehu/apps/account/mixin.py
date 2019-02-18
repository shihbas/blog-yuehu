# coding=utf-8

from django.db import models
from common import constant as common_constant
from common.function import create_random_code


class OpenIdMixin(models.Model):

    @classmethod
    def oid_exists(cls, oid):
        """
            是否存在该oid
        :param oid: oid
        :return:
        """
        return cls.objects.filter(oid=oid).exists()

    oid = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        unique=True
    )

    @property
    def open_id(self):
        if self.oid is None:
            oid = self.create_oid()
        else:
            oid = self.oid
        return oid

    def create_oid(self):
        """
            创建oid
        :return:
        """
        oid = create_random_code(length=10, mode=common_constant.MODE5)
        while self.oid_exists(oid):
            oid = create_random_code(length=10, mode=common_constant.MODE5)
        self.oid = oid
        self.save()
        return oid

    class Meta:
        abstract = True
