# coding=utf-8

from django.test import TestCase
from django.urls import reverse

from article.models import Article, ArticleTag


class ArticleTestCase(TestCase):

    def setUp(self):
        pass

    def test_index_article_list(self):
        """
            首页文章列表测试
        :return:
        """
        Article.create_test_items(params_set={
            "title": "test1",
        }, number=3)

        # response1 = self.client.get("/yuehu/article/api/index_article_list/")
        response1 = self.client.get(reverse("article:index_article_list"))
        self.assertEqual(response1.data.get('code'), "ok")

    def test_index_article_tag_list(self):
        """
            首页标签列表测试
        :return:
        """
        ArticleTag.create_test_items(params_set={
            "name": "123"
        }, number=4)

        response2 = self.client.get(reverse("article:get_index_article_tag_list"))
        self.assertEqual(response2.data.get('code'), "ok")

    def test_show_article_detail(self):
        """
            文章详情页测试
        :return:
        """
        Article.create_test_items(params_set={
            "title": "test1",
            "open_code": "123321"
        }, number=1)

        response = self.client.get(reverse("article:get_article_detail") + "?code=123321")
        self.assertEqual(response.data.get('code'), "ok")

        response1 = self.client.get(reverse("article:get_article_detail"))
        self.assertEqual(response1.data.get('code'), "validate")

        response1 = self.client.get(reverse("article:get_article_detail") + "?code=123456")
        self.assertEqual(response1.data.get('code'), "logic")
