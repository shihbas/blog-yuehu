# coding=utf-8

from django.utils import timezone

from rest_framework.views import APIView
from rest_framework.response import Response

from common.decorators import cms_common, common_validate
from common.fields import date_str_fmt

from banner.models import SlideShow
from banner.serializers.cms import SlideShowListSerializers
from banner.permissions.cms import CMSBannerSlideShowManager


class CMSManageSlideShow(APIView):

    permission_classes = (CMSBannerSlideShowManager,)

    required_fields = ['sort_no', 'title', 'date', 'link']

    type_fields = {
        'sort_no': int,
        'date': date_str_fmt
    }
    logic_fields = {
        'sort_no': (lambda x: 101 > x > 0, "排序no应该介于0-100间")
    }

    @cms_common
    def get(self, request):
        slide_show_ser = SlideShowListSerializers(SlideShow.get_cms_show_list(), many=True)

        return Response(data=slide_show_ser.data)


    @cms_common
    @common_validate(required_fields=required_fields, type_fields=type_fields, logic_fields=logic_fields)
    def post(self, request):
        sort_no = request.data.get("sort_no")
        title = request.data.get("title")
        date = request.data.get("date")
        link = request.data.get("link")
        description = request.data.get("description")
        img = request.data.get("img")

        slide_show = SlideShow.objects.create(
            sort_no=sort_no,
            title=title,
            date=date,
            link=link,
            description=description,
            img=img
        )

        return Response({"created": slide_show.code})

    @cms_common
    @common_validate(required_fields=required_fields, type_fields=type_fields, logic_fields=logic_fields)
    def put(self, request):
        code = request.data.get("code")
        sort_no = request.data.get("sort_no")
        title = request.data.get("title")
        date = request.data.get("date")
        link = request.data.get("link")
        description = request.data.get("description")
        img = request.data.get("img")

        updated = SlideShow.objects.filter(open_code=code).update(
            sort_no=sort_no,
            title=title,
            date=date,
            link=link,
            description=description,
            img=img
        )

        return Response({"updated": updated})

    @cms_common
    def delete(self, request):
        code = request.GET.get("code")

        deleted = SlideShow.objects.filter(open_code=code).update(
            delete_flag=True,
            delete_time=timezone.now()
        )

        return Response({"deleted": deleted})
