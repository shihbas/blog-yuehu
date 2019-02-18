# coding=utf-8

from django.core.management.base import BaseCommand
from django.db.models import Count

from article.models import Article, ArticleCommentReply, ArticleComment

from helper.logs import get_logger

logger = get_logger(__name__)


def comment_binary_search(key, query_list, index, length, max_index):
    if length < 1:
        if query_list[index]['article_id'] == key:
            return query_list[index]['sum_comment']
        else:
            return 0

    if index > max_index or index < 0:
        return 0

    if query_list[index]['article_id'] == key:
        return query_list[index]['sum_comment']

    if length%2==0:
        length = int(length / 2)
    else:
        length = int(length / 2) + 1

    if query_list[index]['article_id'] > key:
        index -= length
        return comment_binary_search(key, query_list, index, length, max_index)
    else:
        index += length
        return comment_binary_search(key, query_list, index, length, max_index)


class Command(BaseCommand):

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # FIXME: 这么更新是有问题的 当更新的同时有人增加或减少了喜欢 会导致数据还是有偏差
        comment_group = ArticleComment.objects.values('article_id').annotate(sum_comment=Count('article_id')).order_by('article_id')
        comment_reply_list = list(ArticleCommentReply.objects.values('article_id').annotate(sum_comment=Count('article_id')).order_by('article_id'))
        comment_aid_list = []

        # 是否能用二分法
        reply_list_length = len(comment_reply_list)
        index = int(reply_list_length/2)
        max_index = reply_list_length - 1

        for item in comment_group:
            if reply_list_length > 0:
                if reply_list_length > 1:
                    item['sum_comment'] += comment_binary_search(item['article_id'], comment_reply_list, index, index, max_index)
                else:
                    if item['article_id'] == comment_reply_list[0]['article_id']:
                        item['sum_comment'] += comment_reply_list[0]['sum_comment']

            Article.objects.filter(id=item['article_id']).update(comment=item['sum_comment'])
            comment_aid_list.append(item['article_id'])

        Article.objects.exclude(id__in=comment_aid_list).update(comment=0)

