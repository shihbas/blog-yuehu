# coding=utf-8

from django.db import models

from base.managers import BaseManager


class BaseModel(models.Model):

    delete_flag = models.BooleanField(
        default=False,
        verbose_name="是否被删除"
    )

    create_time = models.DateTimeField(
        auto_now_add=True,
        verbose_name="创建时间"
    )

    last_update_time = models.DateTimeField(
        auto_now=True,
        verbose_name="最后更新时间"
    )

    delete_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="删除时间"
    )

    objects = BaseManager()

    class Meta:
        abstract = True

    @classmethod
    def create_test_items(cls, params_set: dict={}, number: int=5):
        """
            创建测试用例
        :param number: 创建个数
        :param params_set: 创建项参数集合
        :return:
        """
        if isinstance(params_set, dict) and isinstance(number, int) and 0 < number < 20:
            cls.objects.bulk_create([cls(**params_set) for _ in range(0, number)])
        else:
            raise TypeError(f"TEST: create test {cls.__name__} item parameter error")


class BaseDeleteModel(models.Model):

    delete_flag = models.BooleanField(
        default=False,
        verbose_name="是否被删除"
    )

    delete_time = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="删除时间"
    )

    objects = BaseManager()

    class Meta:
        abstract = True

    @classmethod
    def create_test_items(cls, params_set: dict={}, number: int=5):
        """
            创建测试用例
        :param number: 创建个数
        :param params_set: 创建项参数集合
        :return:
        """
        if isinstance(params_set, dict) and isinstance(number, int) and 0 < number < 20:
            cls.objects.bulk_create([cls(**params_set) for _ in range(0, number)])
        else:
            raise TypeError(f"TEST: create test {cls.__name__} item parameter error")
