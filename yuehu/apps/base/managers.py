# coding=utf-8

from django.db import models


class BaseManager(models.Manager):
    
    def get_queryset(self):
        return super(BaseManager, self).get_queryset().filter(delete_flag=False).defer('delete_flag', 'delete_time')

    def get_queryset_all(self):
        return super(BaseManager, self).get_queryset()

    class Meta:
        abstract = True
