# coding=utf-8

from django.db import models

from common.mixin import OpenCodeMixin

from photowall import constant as photo_wall_constant

from base.models import BaseDeleteModel


class PhotoItem(BaseDeleteModel, OpenCodeMixin):

    # public
    title = models.CharField(max_length=32)

    link = models.CharField(max_length=256)

    sort_no = models.PositiveSmallIntegerField(default=0)

    status = models.PositiveSmallIntegerField(
        default=photo_wall_constant.PHOTO_SHOW_STATUS_NO_DISPLAY,
        choices=photo_wall_constant.PHOTO_SHOW_STATUS_OPTIONS
    )

    description = models.CharField(
        max_length=128,
        blank=True,
        null=True
    )

    is_original = models.BooleanField(default=True)

    # original options

    original_datetime = models.DateTimeField(
        null=True,
        blank=True
    )

    original_place = models.CharField(
        max_length=32,
        null=True,
        blank=True
    )

    # unoriginal options

    source_name = models.CharField(
        max_length=32,
        blank=True,
        null=True
    )

    source_link = models.CharField(
        max_length=256,
        blank=True,
        null=True
    )
