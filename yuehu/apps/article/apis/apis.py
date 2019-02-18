# coding=utf-8

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from common.function import request_objects_pagination
from common.decorators import common_validate
from common.exceptions import ValidateException, LogicException
from common.permissions import IsLogin

from article.models import Article, ArticleTag, ArticleComment, ArticleCommentReply, LikeArticleRelation
from article.serializers.apis import IndexArticleListSerializers, UsualArticleTagListSerializers,\
    ShowArticleDetailSerializers, ArticleCommentItemsSerializers
from article import constant as article_constant

from article.tasks import article_visit_add, article_comment_add, article_comment_reduce, article_like_bind, article_like_canal

from common.decorators import api_common


@api_view(["GET"])
@api_common
def get_index_article_list(request):

    article_list = Article.objects.select_related("author").prefetch_related("article_tag")\
        .filter(status=article_constant.ARTICLE_STATUS_DISPLAY)\
        .order_by("-last_update_time").defer(
        'content',
        'author__avatar',
        'author__avatar_change_date',
        'author__nickname_change_date',
        'author__remark_name',
        'author__date_joined',
        'author__gender',
        'author__register_type',
        'author__is_cms',
        'author__is_active',
        'author__is_staff'
    )

    data = request_objects_pagination(request, article_list, IndexArticleListSerializers)

    return Response(data=data)


@api_view(["GET"])
@api_common
def get_index_article_tag_list(request):

    article_tag_list = ArticleTag.objects.filter(level=0).only("open_code", "name", "level")
    data = UsualArticleTagListSerializers(article_tag_list, many=True).data

    return Response(data=data)


@api_view(["GET"])
@api_common
def get_article_detail(request):

    code = request.GET.get("code", None)

    if request.user.is_authenticated:
        user_id = request.user.id
    else:
        user_id = None

    ve = ValidateException()

    if not code:
        ve.add_message("code", "invalid")

    if ve.is_error():
        raise ve

    article = Article.objects.select_related("author")\
        .filter(open_code=code).defer(
        'description',
        'author__avatar',
        'author__avatar_change_date',
        'author__nickname_change_date',
        'author__remark_name',
        'author__date_joined',
        'author__gender',
        'author__register_type',
        'author__is_cms',
        'author__is_active',
        'author__is_staff'
    ).first()

    if article is None:
        raise LogicException("无效的文章码")

    if user_id:
        is_like = LikeArticleRelation.check_user_like_article(user_id=user_id, article_id=article.id)
    else:
        is_like = False

    article_ser = ShowArticleDetailSerializers(article, context={"is_like": is_like}).data

    # 使用消息队列记录访问log
    article_visit_add.delay(user_id=user_id, article_id=article.pk)

    return Response(data=article_ser)


@api_view(["GET"])
@api_common
def get_index_hot_article_list(request):
    article_list = Article.objects.filter(
        status=article_constant.ARTICLE_STATUS_DISPLAY
    ).values("open_code", "title").order_by("-visit", "-like", "-comment")[:4]
    return Response(data=article_list)


class ApiLikeArticle(APIView):

    permission_classes = (IsLogin,)

    required_fields = ['article_code']


    @api_common
    @common_validate(required_fields=required_fields)
    def post(self, request):
        article_code = request.data.get("article_code")
        user_id = request.user.id
        article_like_bind.delay(user_id=user_id, article_code=article_code)
        return Response(data={
            "created": 1
        })

    @api_common
    @common_validate(required_fields=required_fields)
    def delete(self, request):
        article_code = request.GET.get("article_code")
        user_id = request.user.id

        article_like_canal.delay(user_id=user_id, article_code=article_code)
        return Response(data={
            "deleted": 1
        })

get_article_comments_required_fields = ['article_code', 'page']
get_article_comments_type_fields = {"page": (int, 1)}

@api_view(["GET"])
@api_common
@common_validate(required_fields=get_article_comments_required_fields, type_fields=get_article_comments_type_fields)
def get_article_comments(request):
    article_code = request.GET.get("article_code")
    page = request.GET.get("page")
    page_sum, page, one_page_max, article_comment_set, reply_dict = ArticleComment.get_article_comment_by_code(
        article_code=article_code,
        page=page,
        max_size=article_constant.ARTICLE_COMMENT_PAGE_SIZE_MAX
    )
    article_comment_ser = []
    if page_sum > 0:
        article_comment_ser = ArticleCommentItemsSerializers(article_comment_set, many=True, content=reply_dict).data
    data = {
        "items": article_comment_ser,
        "page_sum": page_sum,
        "page": page,
        "one_page_max": one_page_max
    }
    return Response(data=data)


class ApiCommentArticle(APIView):

    permission_classes = (IsLogin,)

    post_required_fields = ['article_code', 'content']

    post_logic_fields = {
        'content': (lambda x: 1 < len(x) < 100, '内容长度超过100')
    }

    delete_required_fields = ['comment_code']

    @api_common
    @common_validate(required_fields=post_required_fields, logic_fields=post_logic_fields)
    def post(self, request):
        user_id = request.user.id
        article_code = request.data.get("article_code")
        content = request.data.get("content")
        comment_code, article_id = ArticleComment.add_article_comment_by_code(
            user_id=user_id, article_code=article_code, content=content
        )
        article_comment_add.delay(article_id=article_id)
        return Response(data={"created": comment_code})

    @api_common
    @common_validate(required_fields=delete_required_fields)
    def delete(self, request):
        user_id = request.user.id
        comment_code = request.GET.get("comment_code")

        deleted_number, article_id = ArticleComment.delete_comment_by_code(user_id=user_id, comment_code=comment_code)
        article_comment_reduce.delay(article_id=article_id, number=deleted_number)
        return Response(data={"deleted": deleted_number})


class ApiReplyCommentReply(APIView):
    permission_classes = (IsLogin,)

    post_required_fields = ['comment_user_code', 'original_comment_code','content']

    post_logic_filed = {
        'content': (lambda x: 1 < len(x) < 100, '内容长度超过100')
    }

    delete_required_fields = ['reply_comment_code', 'original_comment_code']

    @api_common
    @common_validate(required_fields=post_required_fields, logic_fields=post_logic_filed)
    def post(self, request):
        user_id = request.user.id
        comment_user_code = request.data.get("comment_user_code")
        original_comment_code = request.data.get("original_comment_code")
        content = request.data.get("content")
        reply_code, article_id = ArticleCommentReply.add_article_comment_reply_by_code(
            reply_user_id=user_id,
            comment_user_code=comment_user_code,
            original_comment_code=original_comment_code,
            content=content
        )

        article_comment_add.delay(article_id=article_id)

        return Response(data={"created": reply_code})

    @api_common
    @common_validate(required_fields=delete_required_fields)
    def delete(self, request):
        user_id = request.user.id
        reply_comment_code = request.GET.get("reply_comment_code")
        original_comment_code = request.GET.get("original_comment_code")
        deleted_number, article_id = ArticleCommentReply.delete_article_comment_reply_by_code(
            reply_user_id=user_id,
            reply_comment_code=reply_comment_code,
            original_comment_code=original_comment_code
        )

        article_comment_reduce.delay(article_id=article_id, number=deleted_number)

        return Response(data={"deleted": deleted_number})
