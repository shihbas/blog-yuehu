# coding=utf-8

from rest_framework import serializers

from article.models import Article, ArticleTag, ArticleComment, ArticleCommentReply
from article import constant as article_constant


class UsualArticleTagListSerializers(serializers.ModelSerializer):

    class Meta:
        model = ArticleTag
        fields = ["code", "name", "level"]


class IndexArticleListSerializers(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)
    author_open_id = serializers.SerializerMethodField(read_only=True)

    created = serializers.DateTimeField(source="create_time", format="%Y/%m/%d")
    updated = serializers.DateTimeField(source="last_update_time", format="%Y/%m/%d")
    article_tag_list = serializers.ListField()

    class Meta:
        model = Article
        fields = ["title", "display_description", "list_display_image", "author_name", "author_open_id", "created",
                  "updated", "code", "article_tag_list", "visit", "like", "comment"]

    def __init__(self, instance, *args, **kwargs):

        for item in instance:
            item.article_tag_list = UsualArticleTagListSerializers(
                item.article_tag.all(),
                many=True
            ).data

        super(IndexArticleListSerializers, self).__init__(instance, *args, **kwargs)

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


class ShowArticleDetailSerializers(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)
    author_open_id = serializers.SerializerMethodField(read_only=True)

    created = serializers.DateTimeField(source="create_time", format="%Y/%m/%d")
    updated = serializers.DateTimeField(source="last_update_time", format="%Y/%m/%d")

    is_like = serializers.BooleanField()

    class Meta:
        model = Article
        fields = ["title", "list_display_image", "author_name", "author_open_id", "created",
                  "updated", "code", "content", "edit_type", "visit", "like", "comment", "is_like"]

    def __init__(self, instance, *args, **kwargs):
        context = kwargs.pop("context", {})
        instance.is_like = context.get("is_like", False)
        super(ShowArticleDetailSerializers, self).__init__(instance, *args, **kwargs)

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


class ArticleCommentRelayItemsSerializers(serializers.ModelSerializer):
    commenter_nickname = serializers.SerializerMethodField(read_only=True)
    commenter_code = serializers.SerializerMethodField(read_only=True)

    reply_user_nickname = serializers.SerializerMethodField(read_only=True)
    reply_user_code = serializers.SerializerMethodField(read_only=True)
    reply_user_avatar = serializers.SerializerMethodField(read_only=True)

    created_time = serializers.DateTimeField(source="created", format="%Y/%m/%d %H:%M")

    class Meta:
        model = ArticleCommentReply
        fields = ["commenter_nickname", "commenter_code",
                  "reply_user_nickname", "reply_user_code", "reply_user_avatar",
                  "content", "code", "created_time"]

    def get_commenter_nickname(self, obj):
        return obj.comment_user.display_name

    def get_commenter_code(self, obj):
        return obj.comment_user.oid

    def get_reply_user_nickname(self, obj):
        return obj.reply_user.display_name

    def get_reply_user_code(self, obj):
        return obj.reply_user.oid

    def get_reply_user_avatar(self, obj):
        return obj.reply_user.display_avatar


class ArticleCommentItemsSerializers(serializers.ModelSerializer):
    commenter_nickname = serializers.SerializerMethodField(read_only=True)
    commenter_code = serializers.SerializerMethodField(read_only=True)
    commenter_avatar = serializers.SerializerMethodField(read_only=True)
    created_time = serializers.DateTimeField(source="created", format="%Y/%m/%d %H:%M")
    relay_list = serializers.ListField()

    class Meta:
        model = ArticleComment
        fields = ["commenter_nickname", "commenter_code", "commenter_avatar", "content", "code", "created_time", "relay_list"]

    def __init__(self, instance, *args, **kwargs):
        relay_dict = kwargs.pop("content", {})

        for item in instance:
            item.relay_list = ArticleCommentRelayItemsSerializers(relay_dict.get(item.id, []), many=True).data

        super(ArticleCommentItemsSerializers, self).__init__(instance, *args, **kwargs)


    def get_commenter_nickname(self, obj):
        return obj.user.display_name

    def get_commenter_code(self, obj):
        return obj.user.oid

    def get_commenter_avatar(self, obj):
        return obj.user.display_avatar
