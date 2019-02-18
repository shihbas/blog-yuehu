# coding=utf-8

from django.db import models
from common import constant as common_constant
from common.function import create_random_code


class OpenCodeMixin(models.Model):

    open_code = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        unique=True
    )

    @classmethod
    def open_code_exists(cls, open_code):
        """
            是否存在该open_code
        :param open_code: open_code
        :return:
        """
        return cls.objects.filter(open_code=open_code).exists()

    @property
    def code(self):
        if self.open_code is None:
            open_code = self.create_open_code()
        else:
            open_code = self.open_code
        return open_code

    def create_open_code(self):
        """
            创建open_code
        :return:
        """
        open_code = create_random_code(length=10, mode=common_constant.MODE5)
        while self.open_code_exists(open_code):
            open_code = create_random_code(length=10, mode=common_constant.MODE5)
        self.open_code = open_code
        self.save()
        return open_code

    class Meta:
        abstract = True
