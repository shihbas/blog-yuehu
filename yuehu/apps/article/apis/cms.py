# coding=utf-8

from django.utils import timezone
from django.db.models import Q

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from common.function import request_objects_pagination
from common.exceptions import LogicException
from common.decorators import cms_common, common_validate

from article.models import Article, ArticleTag, ArticleRelationTag
from article.serializers.cms import CMSAllArticleListSerializers, CMSSelfArticleListSerializers, \
    CMSArticleDetailSerializers, CMSUsualArticleTagSerializers, CMSArticleTagManageList
from article.permissions.cms import CMSSelfArticleManager, CMSAllArticleManager, CMSAllTagManager
from article import constant as article_constant


class CMSManageSelfArticleList(APIView):

    permission_classes = (CMSSelfArticleManager,)

    @cms_common
    def get(self, request):
        """
            展示自己的文章
        :param request:
        :return:
        """
        user = request.user
        tag_code = request.GET.get("tag")
        status = request.GET.get("status")
        sort = request.GET.get("sort")

        article_list = Article.objects.prefetch_related("article_tag").filter(
            author=user
        )

        if status:
            try:
                status = int(status)
            except (ValueError, TypeError) as e:
                status = article_constant.ARTICLE_STATUS_WAIT

            article_list = article_list.filter(status=status)
        else:
            article_list = article_list.filter(status__in=article_constant.CMS_SELF_ARTICLE_SHOW_STATUS_LIST)

        if sort == "-created":
            article_list = article_list.order_by("create_time")
        else:
            article_list = article_list.order_by("-create_time")

        if tag_code:
            article_list = article_list.filter(article_tag__open_code=tag_code)

        data = request_objects_pagination(request, article_list, CMSSelfArticleListSerializers)

        return Response(data=data)

    @cms_common
    def put(self, request):
        """
            更新文章状态
        :param request:
        :return:
        """
        user = request.user
        code = request.data.get("code", "")
        status = request.data.get("status", article_constant.ARTICLE_STATUS_WAIT)

        try:
            status = int(status)
        except(ValueError, TypeError) as e:

            status = article_constant.ARTICLE_STATUS_WAIT

        if status not in article_constant.CMS_ALL_ARTICLE_UPDATE_STATUS_LIST:
            raise LogicException("错误的状态😤")

        update_number = Article.objects.filter(
            open_code=code,
            author=user
        ).update(
            status=status
        )
        return Response({"updated": update_number})

    @cms_common
    def delete(self, request):
        """
            删除自己的文章
        :param request:
        :return:
        """
        user = request.user
        code = request.GET.get("code", None)

        delete_number = Article.objects.filter(
            open_code=code,
            author=user
        ).update(
            status=article_constant.ARTICLE_STATUS_NO_DISPLAY
        )
        return Response({"deleted": delete_number})


@api_view(["GET"])
@permission_classes((CMSAllArticleManager,))
@cms_common
def get_cms_all_article_list(request):
    """
        展示所有的文章
    :param request:
    :return:
    """
    tag_code = request.GET.get("tag")
    status = request.GET.get("status")
    sort = request.GET.get("sort")

    article_list = Article.objects.select_related("author").prefetch_related("article_tag")\
        .order_by("-last_update_time")

    if status:
        try:
            status = int(status)
        except (ValueError, TypeError) as e:
            status = article_constant.ARTICLE_STATUS_WAIT

        article_list = article_list.filter(status=status)
    else:
        article_list = article_list.filter(status__in=article_constant.CMS_ALL_ARTICLE_SHOW_STATUS_LIST)

    if sort == "-created":
        article_list = article_list.order_by("create_time")
    else:
        article_list = article_list.order_by("-create_time")

    if tag_code:
        article_list = article_list.filter(article_tag__open_code=tag_code)

    data = request_objects_pagination(request, article_list, CMSAllArticleListSerializers)

    return Response(data=data)


class CMSManageSelfArticleDetail(APIView):

    permission_classes = (CMSSelfArticleManager,)

    post_required_fields = ['title', 'content', 'edit_type']

    put_required_fields = ['title', 'content']

    post_type_fields = {
        'edit_type': int
    }
    post_logic_fields = {
        'edit_type': (lambda x: x in article_constant.ARTICLE_EDIT_ALLOW_LIST, "文本编辑类型尚未开发")
    }

    @cms_common
    def get(self, request):
        user = request.user
        code = request.GET.get("code")

        article = Article.objects.filter(
            author=user,
            open_code=code,
            status__in=article_constant.CMS_SELF_ARTICLE_SHOW_STATUS_LIST
        ).first()

        if article is None:
            raise LogicException("这不是你的文章呦")

        article_ser = CMSArticleDetailSerializers(article)

        return Response(article_ser.data)

    @cms_common
    @common_validate(required_fields=post_required_fields, type_fields=post_type_fields, logic_fields=post_logic_fields)
    def post(self, request):
        user = request.user
        title = request.data.get("title", "")
        description = request.data.get("description", "")
        display_image = request.data.get("display_image", "")
        content = request.data.get("content", "")
        edit_type = request.data.get("edit_type", "")

        article = Article.objects.create(
            title=title,
            description=description,
            display_image=display_image,
            content=content,
            status=article_constant.ARTICLE_STATUS_WAIT,
            author=user,
            edit_type=edit_type
        )

        return Response({"created": article.code})

    @cms_common
    @common_validate(required_fields=put_required_fields)
    def put(self, request):
        user = request.user
        code = request.data.get("code", "")
        title = request.data.get("title", "")
        description = request.data.get("description", "")
        display_image = request.data.get("display_image", "")
        content = request.data.get("content", "")

        update_number = Article.objects.filter(
            open_code=code,
            author=user
        ).update(
            title=title,
            description=description,
            display_image=display_image,
            content=content,
            last_update_time=timezone.now()
        )
        return Response({"updated": update_number})


class CMSManageAllArticleDetail(APIView):

    permission_classes = (CMSAllArticleManager,)

    @cms_common
    def get(self, request):
        code = request.GET.get("code")

        article = Article.objects.filter(open_code=code).first()

        if article is None:
            raise LogicException("文章不存在啊！")

        article_ser = CMSArticleDetailSerializers(article)

        return Response(article_ser.data)

    @cms_common
    def put(self, request):
        """
            更新文章状态
        :param request:
        :return:
        """
        code = request.data.get("code", "")
        status = request.data.get("status", article_constant.ARTICLE_STATUS_WAIT)

        try:
            status = int(status)
        except(ValueError, TypeError) as e:
            status = article_constant.ARTICLE_STATUS_WAIT

        if status not in article_constant.CMS_ALL_ARTICLE_UPDATE_STATUS_LIST:
            raise LogicException("错误的状态😤")

        update_number = Article.objects.filter(
            open_code=code,
        ).update(
            status=status
        )
        return Response({"updated": update_number})

    @cms_common
    def delete(self, request):
        code = request.GET.get("code")

        delete_number = Article.objects.filter(
            open_code=code
        ).update(
            delete_flag=True,
            delete_time=timezone.now()
        )
        return Response({"deleted": delete_number})


class CMSSetArticleTagManage(APIView):

    permission_classes = (CMSSelfArticleManager,)

    @cms_common
    def get(self, request):

        article_tags = ArticleTag.objects.all()
        article_tags_ser = CMSUsualArticleTagSerializers(article_tags, many=True)
        return Response(article_tags_ser.data)

    @cms_common
    def put(self, request):
        article_code = request.data.get("article_code")
        tag_code_list = request.data.get("tag_code_list")

        article = Article.objects.filter(open_code=article_code).first()

        if article is None:
            raise LogicException("这个文章不存在吽")

        article_tag_set = ArticleTag.objects.filter(open_code__in=tag_code_list)
        article_tag_count = len(article_tag_set)
        if article_tag_count == 0:
            raise LogicException("标签不存在吽")
        if article_tag_count > 3:
            raise LogicException("标签不得多于三个")

        article.article_tag.clear()

        ArticleRelationTag.objects.bulk_create(
            [ArticleRelationTag(article_id=article.id, tag_id=tag.id) for tag in article_tag_set]
        )

        return Response({"add": "success"})


@api_view(["GET"])
@permission_classes((CMSSelfArticleManager,))
@cms_common
def get_top_article_tag_list(request):
    article_tags = ArticleTag.objects.filter(level=0).all()
    article_tags_ser = CMSUsualArticleTagSerializers(article_tags, many=True)
    return Response(article_tags_ser.data)


@api_view(["GET"])
@permission_classes((CMSSelfArticleManager,))
@cms_common
def get_all_tag_in_top(request):
    """
        根据顶级标签查询该标签组下的所有标签
    :param request:
    :return:
    """
    code = request.GET.get("code")

    top_tag = ArticleTag.objects.filter(level=0, open_code=code).first()

    if top_tag is None:
        raise LogicException("没有该顶级标签code")

    tags = ArticleTag.objects.filter(Q(root_tag=top_tag) | Q(id=top_tag.id))
    tags_ser = CMSUsualArticleTagSerializers(tags, many=True)
    return Response(tags_ser.data)


class CMSArticleTagManage(APIView):
    """
        管理tag
    """

    permission_classes = (CMSAllTagManager,)

    @cms_common
    def get(self, request):
        code = request.GET.get("code")

        top_tag = ArticleTag.objects.filter(level=0, open_code=code).first()
        if top_tag is None:
            raise LogicException("没有该顶级标签code")

        tags = ArticleTag.objects.filter(Q(root_tag=top_tag) | Q(id=top_tag.id))
        tags_ser = CMSArticleTagManageList(tags, many=True)
        return Response(tags_ser.data)

    @cms_common
    def post(self, request):
        top_code = request.data.get("top_code")
        level = request.data.get("level")
        name = request.data.get("name")
        display_image = request.data.get("display_image")
        description = request.data.get("description")

        try:
            level = int(level)
            if level < 0:
                raise ValueError
        except (ValueError, TypeError) as e:
            raise LogicException("level参数类型错误")

        if level > 0:
            top_tag = ArticleTag.objects.filter(open_code=top_code).first()
        else:
            top_tag = None

        if top_tag is None and level > 0:
            raise LogicException("top_code参数无效")

        article_tag = ArticleTag(
            name=name,
            level=level,
            display_image=display_image,
            description=description,
            root_tag=top_tag
        )
        article_tag.save()
        return Response({"created": article_tag.code})

    @cms_common
    def put(self, request):
        code = request.data.get("code")
        name = request.data.get("name")
        display_image = request.data.get("display_image")
        description = request.data.get("description")

        updated_number = ArticleTag.objects.filter(open_code=code).update(
            name=name,
            display_image=display_image,
            description=description
        )
        return Response({"updated": updated_number})

    @cms_common
    def delete(self, request):
        code = request.GET.get("code")
        tag = ArticleTag.objects.filter(open_code=code).first()

        # todo: 标签的父子关系 以及根叶关系暂时只有两层 当有多层时删除变得很复杂暂时没有做

        if tag is None:
            raise LogicException("code无效")

        tag_id_list = []
        if tag.level == 0:
            tag_id_list = ArticleTag.objects.filter(root_tag_id=tag.id).values_list("id", flat=True)
            tag_id_list = list(tag_id_list)

        tag_id_list.append(tag.id)
        relation_deleted = ArticleRelationTag.objects.filter(tag_id__in=tag_id_list).delete()

        deleted = ArticleTag.objects.filter(id__in=tag_id_list).update(
            delete_flag=True,
            delete_time=timezone.now()
        )

        return Response({"deleted": deleted})
