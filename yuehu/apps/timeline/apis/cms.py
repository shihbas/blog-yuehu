# coding=utf-8

from django.utils import timezone

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from common.decorators import cms_common, common_validate
from common.exceptions import LogicException
from common.fields import date_str_fmt

from timeline.models import TimelineLine, TimelineItem
from timeline.serializers.cms import CMSAllTimeLineListSerializer
from timeline.permissions.cms import CMSPhotoWallManager

class CMSTimeLine(APIView):

    permission_classes = (CMSPhotoWallManager,)

    required_fields = ['title', 'year']

    type_fields = {
        'year': int
    }
    logic_fields = {
        'year': (lambda x: x > 2017, "时间线只能创建大于2017年之后的")
    }

    @cms_common
    def get(self, request):

        timeline_set = TimelineLine.objects.prefetch_related("timeline_items").all().order_by("-year")

        timeline_ser = CMSAllTimeLineListSerializer(timeline_set, many=True)

        return Response(data=timeline_ser.data)

    @cms_common
    @common_validate(required_fields=required_fields, type_fields=type_fields, logic_fields=logic_fields)
    def post(self, request):
        year = request.data.get("year")
        title = request.data.get("title")
        content = request.data.get("content")

        if TimelineLine.objects.filter(year=year).exists():
            raise LogicException(f"{year}年份的时间线已经存在了")

        timeline = TimelineLine.objects.create(
            year=year,
            title=title,
            content=content
        )
        return Response({"created": timeline.code})

    @cms_common
    @common_validate(required_fields=required_fields, type_fields=type_fields, logic_fields=logic_fields)
    def put(self, request):
        code = request.data.get("code")
        year = request.data.get("year")
        title = request.data.get("title")
        content = request.data.get("content")

        updated = TimelineLine.objects.filter(open_code=code).update(
            year=year,
            title=title,
            content=content
        )
        return Response({"updated": updated})

    @cms_common
    def delete(self, request):
        code = request.GET.get("code")

        timeline = TimelineLine.objects.filter(open_code=code).first()
        if timeline is None:
            raise LogicException("时间线删除失败，code无效")

        return Response({"deleted": timeline.delete_timeline()})


class CMSTimeLineItem(APIView):

    permission_classes = (CMSPhotoWallManager,)

    required_fields = ['title', 'date', 'code']

    type_fields = {
        'date': date_str_fmt
    }

    @cms_common
    @common_validate(required_fields=required_fields, type_fields=type_fields)
    def post(self, request):
        code = request.data.get("code")
        date = request.data.get("date")
        title = request.data.get("title")
        content = request.data.get("content")

        timeline = TimelineLine.objects.filter(open_code=code).first()
        if timeline is None:
            raise LogicException(f"code为{code}的时间线不存在")

        if timeline.year != date.year:
            raise LogicException(f"不能在年份为{timeline.year}创建的{date}节点项")

        if TimelineItem.objects.filter(date=date).exists():
            raise LogicException(f"{date}的时间项已经存在了")

        timeline_item = TimelineItem.objects.create(
            date=date,
            title=title,
            content=content,
            timeline=timeline
        )
        return Response({"created": timeline_item.code})

    @cms_common
    @common_validate(required_fields=required_fields, type_fields=type_fields)
    def put(self, request):
        code = request.data.get("code")
        title = request.data.get("title")
        content = request.data.get("content")

        updated = TimelineItem.objects.filter(open_code=code).update(
            title=title,
            content=content
        )
        return Response({"updated": updated})

    @cms_common
    def delete(self, request):
        code = request.GET.get("code")

        updated = TimelineItem.objects.filter(open_code=code).update(
            delete_flag=True,
            delete_time=timezone.now()
        )

        return Response({"deleted": updated})
