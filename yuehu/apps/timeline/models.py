# coding=utf-8

from django.db import models, transaction
from django.utils import timezone

from base.models import BaseDeleteModel

from common.mixin import OpenCodeMixin

from helper.logs import get_logger

logger = get_logger(__name__)


class TimelineLine(BaseDeleteModel, OpenCodeMixin):

    year = models.PositiveSmallIntegerField()

    title = models.CharField(
        default="",
        max_length=64
    )

    content = models.CharField(
        default="",
        max_length=512
    )

    def delete_timeline(self):
        try:
            with transaction.atomic():

                updated = TimelineItem.objects.filter(timeline_id=self.id).update(
                    delete_flag=True,
                    delete_time=timezone.now()
                )
                self.delete_time = timezone.now()
                self.delete_flag = True
                self.save()
                return updated + 1
        except Exception as e:
            logger.error(e)

        return 0


class TimelineItem(BaseDeleteModel, OpenCodeMixin):

    date = models.DateField()

    title = models.CharField(
        default="",
        max_length=64
    )

    content = models.CharField(
        default="",
        max_length=512
    )

    timeline = models.ForeignKey(
        "timeline.TimelineLine",
        on_delete=models.PROTECT,
        related_name="timeline_items"
    )
