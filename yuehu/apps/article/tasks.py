# coding=utf-8

from yuehu.celery_yuehu import app

from helper.logs import visit_article_log

from article.models import LikeArticleRelation, Article


@app.task(bind=True)
def article_visit_add(self, user_id, article_id: int):
    """
        用户访问文章
    :param user_id: 用户ID
    :param article_id: 文章ID
    :return:
    """
    Article.visited_article(article_id)
    visit_article_log(user_id=user_id, article_id=article_id)
    return 1


@app.task(bind=True)
def article_like_bind(self, user_id, article_code):
    """
        用户点击喜欢文章
    :param self:
    :param user_id:
    :param article_code:
    :return:
    """
    return LikeArticleRelation.bind_like_article_by_code(user_id, article_code)


@app.task(bind=True)
def article_like_canal(self, user_id, article_code):
    """
        用户点击取消喜欢文章
    :param self:
    :param user_id:
    :param article_code:
    :return:
    """
    return LikeArticleRelation.remove_like_article_by_code(user_id=user_id, article_code=article_code)


@app.task(bind=True)
def article_comment_add(self, article_id, number=1):
    """
        文章评论增加
    :param self:
    :param article_id:
    :param number:
    :return:
    """
    Article.article_comment_add(article_id=article_id, number=number)
    return number


@app.task(bind=True)
def article_comment_reduce(self, article_id, number=1):
    """
        文章评论减少
    :param self:
    :param article_id:
    :param number:
    :return:
    """
    Article.article_comment_reduce(article_id=article_id, number=number)
    return number
