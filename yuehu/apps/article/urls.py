# coding=utf-8

from django.urls import path

from article.apis import apis, cms


app_name = "article"

api_urlpatterns = [
    path('api/index_article_list/', apis.get_index_article_list, name="index_article_list"),
    path('api/index_article_tag_list/', apis.get_index_article_tag_list, name="get_index_article_tag_list"),
    path('api/index_article_hot_list/', apis.get_index_hot_article_list, name='api_index_hot_article_list'),
    path('api/get_article_detail/', apis.get_article_detail, name="get_article_detail"),
    path('api/article_like/', apis.ApiLikeArticle.as_view(), name="api_like_article"),
    path('api/article_comment/', apis.ApiCommentArticle.as_view(), name="api_comment_article"),
    path('api/article_reply_comment/', apis.ApiReplyCommentReply.as_view(), name="api_reply_comment_article"),
    path('api/article_comment_list/', apis.get_article_comments, name="api_article_comment_list"),
]

cms_urlpatterns = [
    path('cms/self_article_list/', cms.CMSManageSelfArticleList.as_view(), name="get_cms_self_article_list"),
    path('cms/self_article_detail/', cms.CMSManageSelfArticleDetail.as_view(), name="cms_self_article_detail"),
    path('cms/self_article_detail_set_tag/', cms.CMSSetArticleTagManage.as_view(), name="cms_self_article_set_tag"),

    path('cms/all_article_list/', cms.get_cms_all_article_list, name="get_cms_all_article_list"),
    path('cms/all_article_detail/', cms.CMSManageAllArticleDetail.as_view(), name="cms_all_article_detail"),

    path('cms/top_article_tag_list/', cms.get_top_article_tag_list, name="get_top_article_tag_list"),
    path('cms/all_tag_in_top/', cms.get_all_tag_in_top, name='get_all_tag_in_top'),
    path('cms/all_tag_manage/', cms.CMSArticleTagManage.as_view(), name="all_tag_manage"),
]

urlpatterns = api_urlpatterns + cms_urlpatterns
