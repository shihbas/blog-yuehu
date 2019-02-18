# coding=utf-8

from django.test import TestCase
from django.urls import reverse

from banner.models import SlideShow


class SlideShowTestCase(TestCase):

    def setUp(self):
        pass

    def test_index_slide_show_list(self):
        """
            首页文章列表测试
        :return:
        """
        SlideShow.create_test_items(params_set={
            "title": "test1",
        }, number=3)

        response1 = self.client.get(reverse("banner:get_slide_show_list"))
        self.assertEqual(response1.data.get('code'), "ok")
