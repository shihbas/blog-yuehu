# coding=utf-8

from django.db import models, transaction
from django.utils import timezone

from base.models import BaseModel, BaseDeleteModel

from common.mixin import OpenCodeMixin
from common.exceptions import LogicException
from common.function import pagination

from account.models import User

from article import constant as article_constant


class Article(BaseModel, OpenCodeMixin):

    title = models.CharField(
        null=True,
        blank=True,
        max_length=64,
    )

    description = models.CharField(
        max_length=128,
        default=""
    )
    # 列表信息中展示的图片
    display_image = models.CharField(
        max_length=256,
        default=""
    )

    content = models.TextField(default="")

    status = models.PositiveSmallIntegerField(
        default=article_constant.ARTICLE_STATUS_WAIT,
        choices=article_constant.ARTICLE_STATUS_CHOICES
    )

    edit_type = models.PositiveSmallIntegerField(
        default=article_constant.ARTICLE_EDIT_RICH_TEXT,
        choices=article_constant.ARTICLE_EDIT_CHOICES
    )

    author = models.ForeignKey(
        "account.User",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="account_article_set"
    )

    article_tag = models.ManyToManyField(
        "article.ArticleTag",
        through="article.ArticleRelationTag"
    )

    # 文章的数据

    ## 浏览
    visit = models.IntegerField(
        default=0
    )
    ## 点赞
    like = models.IntegerField(
        default=0
    )
    ## 评论
    comment = models.IntegerField(
        default=0
    )

    @classmethod
    def visited_article(cls, article_id:int):
        """
            文章被浏览
        :param article_id:
        :return:
        """
        with transaction.atomic():
            article = cls.objects.select_for_update().only("visit").filter(id=article_id).first()
            if article is None:
                return 0
            article.visit += 1
            article.save()
            return 1

    @classmethod
    def article_comment_add(cls, article_id:int, number:int):
        with transaction.atomic():
            article = cls.objects.select_for_update().only("comment").filter(id=article_id).first()
            if article is None:
                return 0
            article.comment += number
            article.save()
            return 1

    @classmethod
    def article_comment_reduce(cls, article_id:int, number:int):
        with transaction.atomic():
            article = cls.objects.select_for_update().only("comment").filter(id=article_id).first()
            if article is None:
                return 0
            article.comment -= number
            article.save()
            return 1

    @property
    def list_display_image(self):
        return self.display_image if self.display_image else article_constant.DEFAULT_ARTICLE_DISPLAY_IMAGE

    @property
    def display_description(self):
        return self.description if self.description else article_constant.DEFAULT_ARTICLE_DESCRIPTION


class ArticleTag(BaseDeleteModel, OpenCodeMixin):

    name = models.CharField(
        null=True,
        blank=True,
        max_length=64,
    )

    description = models.CharField(
        max_length=128,
        default=""
    )

    display_image = models.CharField(
        max_length=256,
        default="",
        blank=True,
        null=True
    )

    level = models.IntegerField(
        default=0
    )

    root_tag = models.ForeignKey(
        "article.ArticleTag",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="all_tag_set"
    )


class ArticleRelationTag(models.Model):

    tag = models.ForeignKey(
        "article.ArticleTag",
        on_delete=models.PROTECT
    )

    article = models.ForeignKey(
        "article.Article",
        on_delete=models.PROTECT
    )


class LikeArticleRelation(models.Model):
    """
        喜欢文章关系
    """
    user_id = models.IntegerField()
    article_id = models.IntegerField()
    like_datetime = models.DateTimeField(blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    @classmethod
    def bind_like_article_by_code(cls, user_id, article_code):
        """
            喜欢文章标记 通过文章code
        :param user_id: 用户对象
        :param article_code: 文章code
        :return:
        """
        article = Article.objects.filter(open_code=article_code).only('id', 'like').first()
        if article is None:
            return 0
        obj, created = cls.objects.get_or_create(user_id=user_id, article_id=article.id, defaults={
            "like_datetime": timezone.now()
        })

        if created:
            article.like += 1
            article.save()
        elif obj.is_delete:
            obj.is_delete = False
            obj.save()
            article.like += 1
            article.save()
        else:
            # 不是新创建并且没有被删除的 不需要增加like数
            return 0

        return 1

    @classmethod
    def remove_like_article_by_code(cls, user_id, article_code):
        """
            取消喜欢文章标记 通过文章code
        :param user_id:
        :param article_code:
        :return:
        """
        article = Article.objects.filter(open_code=article_code).only('id', 'like').first()
        if article is None:
            return 0

        relation = cls.objects.filter(user_id=user_id, article_id=article.id, is_delete=False).first()
        if relation is None:
            return 0

        relation.is_delete = True
        relation.save()

        article.like -= 1
        article.save()

        return 1

    @classmethod
    def check_user_like_article(cls, user_id, article_id):
        """
            校验是否用户喜欢该文章
        :param user_id:
        :param article_id:
        :return:
        """
        return cls.objects.filter(user_id=user_id, article_id=article_id, is_delete=False).exists()


class ArticleComment(BaseDeleteModel, OpenCodeMixin):
    """
        文章评论
    """

    article = models.ForeignKey(
        "article.Article",
        on_delete=models.PROTECT,
        related_name="comment_article_set"
    )

    user = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="account_article_comment_set"
    )

    content = models.CharField(
        max_length=200,
        default=""
    )

    created = models.DateTimeField(auto_now_add=True)


    @classmethod
    def get_article_comment_by_code(cls, article_code, page, max_size):

        article = Article.objects.filter(open_code=article_code).only("id").first()
        if article is None:
            return 0, 1, max_size, [], {}

        return cls.get_article_comment_by_id(article.id, page=page, max_size=max_size)


    @classmethod
    def get_article_comment_by_id(cls, article_id, page, max_size):
        """
            获取文章评论 article_id
        :param article_id:
        :param page:
        :param max_size:
        :return:
        """
        article_comment_set = []
        reply_dict = {}
        article_comment_number = cls.objects.filter(article_id=article_id).count()
        # 分页
        _start, _end, page_sum, page, one_page_max = pagination(article_comment_number, page, max_size)
        if article_comment_number > 0:
            article_comment_set = cls.objects.select_related("user").only(
                "user__nickname", "user__email", "user__oid", "user__username", "user__avatar",
                "content", "open_code", "created", "id"
            ).filter(
                article_id=article_id
            ).order_by("-created")[_start: _end]

            article_comment_id_list = [item.id for item in article_comment_set]

            # 获取评论下的回复
            if article_comment_id_list:
                reply_dict = ArticleCommentReply.get_article_comment_by_pk_list(comment_id_list=article_comment_id_list)
        return page_sum, page, one_page_max, article_comment_set, reply_dict


    @classmethod
    def add_article_comment_by_code(cls, user_id, article_code, content):
        """
            增加评论 通过code
        :param user_id:
        :param article_code:
        :param content:
        :return:
        """
        article = Article.objects.filter(open_code=article_code).only("id").first()
        if article is None:
            raise LogicException("无效的文章code")
        comment = cls(
            article_id=article.id,
            user_id=user_id,
            content=content
        )
        comment.save()
        return comment.code, article.id


    @classmethod
    def delete_comment_by_code(cls, user_id, comment_code):
        """
            删除评论 通过code
        :param user_id:
        :param comment_code:
        :return:
        """
        comment = cls.objects.filter(user_id=user_id, open_code=comment_code).only("id", "article_id").first()
        if comment is None:
            raise LogicException("无效的评论code")
        deleted_number = ArticleCommentReply.delete_all_article_comment_reply_by_id(comment.id)

        deleted_number += cls.objects.filter(
            user_id=user_id, open_code=comment_code
        ).update(
            delete_flag=True,
            delete_time=timezone.now()
        )

        return deleted_number, comment.article_id



class ArticleCommentReply(BaseDeleteModel, OpenCodeMixin):
    """
        文章评论回复
    """

    article = models.ForeignKey(
        "article.Article",
        on_delete=models.PROTECT,
        related_name="reply_article_comment_set"
    )

    original_comment = models.ForeignKey(
        "article.ArticleComment",
        on_delete=models.PROTECT,
        related_name="reply_comment_set"
    )
    # 评论者
    comment_user = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="account_in_comment_reply_set"
    )
    # 回复者
    reply_user = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        related_name="account_article_comment_reply_set"
    )
    content = models.CharField(
        max_length=200,
        default=""
    )
    created = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_article_comment_by_pk_list(cls, comment_id_list):
        """
            获取评论的回复dict
        :param comment_id_list:
        :return:
        """
        article_comment_reply_set =  ArticleCommentReply.objects.select_related("comment_user", "reply_user").only(
            "comment_user__nickname", "comment_user__email", "comment_user__oid", "comment_user__username",
            "reply_user__nickname", "reply_user__email", "reply_user__oid", "reply_user__username", "reply_user__avatar",
            "content", "open_code", "created", "original_comment_id"
        ).filter(original_comment_id__in=comment_id_list).order_by("-created")

        article_comment_reply_dict = dict()
        for item in article_comment_reply_set:
            if item.original_comment_id in article_comment_reply_dict:
                article_comment_reply_dict[item.original_comment_id].append(item)
            else:
                article_comment_reply_dict[item.original_comment_id] = [item]

        return article_comment_reply_dict


    @classmethod
    def add_article_comment_reply_by_code(cls, reply_user_id, comment_user_code, original_comment_code, content):
        """
            增加评论回复 通过code
        :param reply_user_id: 回复者ID
        :param comment_user_code: 原评论用户code
        :param original_comment_code: 原评论code
        :param content: 回复内容
        :return:
        """
        article_comment = ArticleComment.objects.filter(open_code=original_comment_code).only("id", "article_id").first()
        if article_comment is None:
            raise LogicException("无效的评论code")

        comment_user = User.objects.filter(oid=comment_user_code).only("id").first()

        if comment_user is None:
            raise LogicException("无效的用户code")

        comment = cls(
            article_id=article_comment.article_id,
            original_comment_id=article_comment.id,
            reply_user_id=reply_user_id,
            comment_user_id=comment_user.id,
            content=content
        )

        comment.save()
        return comment.code, article_comment.article_id


    @classmethod
    def delete_all_article_comment_reply_by_id(cls, original_comment_id):
        """
            删除某个评论下的所有回复
        :param original_comment_id:
        :return:
        """
        deleted_number = cls.objects.filter(
            original_comment_id=original_comment_id,
        ).update(
            delete_flag=True,
            delete_time=timezone.now()
        )
        return deleted_number

    @classmethod
    def delete_article_comment_reply_by_code(cls, reply_user_id, reply_comment_code, original_comment_code):
        """
            删除某个评论下的某个回复
        :param reply_user_id:
        :param reply_comment_code:
        :param original_comment_code:
        :return:
        """
        article_comment = ArticleComment.objects.filter(open_code=original_comment_code).only("id", "article_id").first()

        if article_comment is None:
            raise LogicException("无效的评论code")

        deleted_number = cls.objects.filter(
            original_comment_id=article_comment.id,
            reply_user_id=reply_user_id,
            open_code=reply_comment_code
        ).update(
            delete_flag=True,
            delete_time=timezone.now()
        )

        return deleted_number, article_comment.article_id
