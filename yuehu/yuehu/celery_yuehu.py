# coding=utf-8

from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yuehu.settings')

app = Celery('celery_yuehu')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(settings.PROJECT_APPS)

app.conf.task_routes = {
    'article.tasks.article_visit_*': {'queue': 'yuehu-article-visit'},
    'article.tasks.article_like_*': {'queue': 'yuehu-article-like'},
    'article.tasks.article_comment_*': {'queue': 'yuehu-article-comment'},
}
