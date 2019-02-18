# coding=utf-8

from rest_framework import serializers

from article.models import Article, ArticleTag
from article import constant as article_constant


class CMSUsualArticleTagSerializers(serializers.ModelSerializer):

    class Meta:
        model = ArticleTag
        fields = ["code", "name", "level"]


class CMSSelfArticleListSerializers(serializers.ModelSerializer):

    created = serializers.DateTimeField(source="create_time", format="%Y/%m/%d %H:%M:%S")
    updated = serializers.DateTimeField(source="last_update_time", format="%Y/%m/%d %H:%M:%S")
    article_tag_list = serializers.ListField()

    class Meta:
        model = Article
        fields = ["title", "created", "code", "updated", "article_tag_list", "status", "edit_type", "visit", "like", "comment"]

    def __init__(self, instance, *args, **kwargs):

        for item in instance:
            item.article_tag_list = CMSUsualArticleTagSerializers(item.article_tag.all(), many=True).data

        super(CMSSelfArticleListSerializers, self).__init__(instance, *args, **kwargs)


class CMSAllArticleListSerializers(serializers.ModelSerializer):

    created = serializers.DateTimeField(source="create_time", format="%Y/%m/%d %H:%M:%S")
    updated = serializers.DateTimeField(source="last_update_time", format="%Y/%m/%d %H:%M:%S")
    author_name = serializers.SerializerMethodField(read_only=True)
    author_open_id = serializers.SerializerMethodField(read_only=True)
    article_tag_list = serializers.ListField()

    class Meta:
        model = Article
        fields = ["title", "created", "code", "updated", "author_name", "author_open_id", "article_tag_list", "status",
                  "edit_type", "visit", "like", "comment"]

    def __init__(self, instance, *args, **kwargs):

        for item in instance:
            item.article_tag_list = CMSUsualArticleTagSerializers(item.article_tag.all(), many=True).data

        super(CMSAllArticleListSerializers, self).__init__(instance, *args, **kwargs)

    def get_author_name(self, obj):
        """
             获取作者名
        :param obj:
        :return:
        """
        if obj.author:
            return obj.author.display_name
        else:
            return None

    def get_author_open_id(self, obj):
        """
            获取作者open id
        :param obj:
        :return:
        """
        if obj.author:
            return obj.author.open_id
        else:
            return None


class CMSArticleDetailSerializers(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = ["title", "description", "display_image", "content", "code", "edit_type"]

    def __init__(self, instance, *args, **kwargs):

        super(CMSArticleDetailSerializers, self).__init__(instance, *args, **kwargs)


class CMSArticleTagManageList(serializers.ModelSerializer):

    class Meta:
        model = ArticleTag
        fields = ["code", "name", "level", "description", "display_image"]
