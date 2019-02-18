# coding=utf-8

from django.core.management.base import BaseCommand
from django.db.models import Count

from article.models import Article, LikeArticleRelation

from helper.logs import get_logger

logger = get_logger(__name__)


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # FIXME: 这么更新是有问题的 当更新的同时有人增加或减少了喜欢 会导致数据还是有偏差
        like_group = LikeArticleRelation.objects.filter(is_delete=False).values('article_id').annotate(sum_like=Count('article_id'))
        like_aid_list = []
        for item in like_group:
            Article.objects.filter(id=item['article_id']).update(like=item['sum_like'])
            like_aid_list.append(item['article_id'])

        Article.objects.exclude(id__in=like_aid_list).update(like=0)



