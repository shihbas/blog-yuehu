# coding=utf-8

from article.models import ArticleTag

from django.template import loader
from django.conf import settings

from common.function import send_email_admin_format_html

from helper.logs import get_logger

logger = get_logger(__name__)


def find_article_tag_root(article_tag_code):
    """
        根据code对寻找两个标签id
    :param article_tag_code: 标签code
    :return:
    """
    root_tag_id = None
    article_tag_id = None
    if article_tag_code:
        article_tag = ArticleTag.objects.filter(open_code=article_tag_code).first()
        if article_tag:
            root_tag_id = article_tag.root_tag_id
            article_tag_id = article_tag.id
            # 当为根节点时 root_tag_id 为 None
            if root_tag_id is None:
                root_tag_id = article_tag.id

    return root_tag_id, article_tag_id


def send_email_html_new_comment(article_code):
    """
        发送新评论通知邮件 (TODO: 18-01-24 暂时没有增加)
    :param article_code:
    :return:
    """
    tmp = loader.get_template("EmailArticleComment.html")
    msg = tmp.render({"domain_name": settings.DOMAIN_NAME, "article_code": article_code})
    return send_email_admin_format_html("新评论通知", msg)
