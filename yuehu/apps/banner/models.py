# coding=utf-8

from django.db import models

from base.models import BaseDeleteModel

from common.mixin import OpenCodeMixin

from banner import constant as banner_constant


class SlideShow(BaseDeleteModel, OpenCodeMixin):

    sort_no = models.PositiveSmallIntegerField(
        default=1
    )

    title = models.CharField(
        max_length=64,
        default=''
    )

    date = models.DateField()

    description = models.CharField(
        max_length=128,
        default=""
    )

    img = models.CharField(
        max_length=256,
        default=""
    )

    link = models.CharField(
        max_length=256,
        default=""
    )

    @classmethod
    def get_show_list(cls):
        return cls.objects.order_by("sort_no")[:5]

    @classmethod
    def get_cms_show_list(cls):
        return cls.objects.order_by("sort_no")

    @property
    def display_img(self):
        return self.img if self.img else banner_constant.DEFAULT_SLIDE_SHOW_DISPLAY_IMAGE

