# coding=utf-8

from django.utils import timezone

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from common.decorators import cms_common, common_validate
from common.function import request_objects_pagination
from common.exceptions import LogicException
from common.fields import datetime_str_fmt_utc8

from photowall.models import PhotoItem
from photowall.serializers.cms import CMSPhotoItemSerializers, CMSPreviewPhotoWallSerializers
from photowall.permissions.cms import CMSPhotoWallManager
from photowall import constant as photowall_constant


class CMSManagePhotoWall(APIView):

    permission_classes = (CMSPhotoWallManager,)

    required_fields = ['title', 'link', 'is_original', 'sort_no']

    type_fields = {
        'sort_no': (int, 1),
        'is_original': (bool, False),
    }
    logic_fields = {
        'sort_no': (lambda x: x > 0, "不能小于0")
    }

    @cms_common
    def get(self, request):

        query_set = PhotoItem.objects.all().order_by('sort_no')

        data = request_objects_pagination(request, query_set, CMSPhotoItemSerializers)

        return Response(data=data)

    @cms_common
    @common_validate(required_fields=required_fields, type_fields=type_fields, logic_fields=logic_fields)
    def post(self, request):
        title = request.data.get("title")
        link = request.data.get("link")
        sort_no = request.data.get("sort_no")
        description = request.data.get("description")
        is_original = request.data.get("is_original")
        original_time = request.data.get("original_time")
        original_place = request.data.get("original_place")
        source_name = request.data.get("source_name")
        source_link = request.data.get("source_link")

        if is_original:
            try:
                original_time = datetime_str_fmt_utc8(original_time)
            except (ValueError, TypeError):
                raise LogicException("原创必须增加拍摄时间")
            photo = PhotoItem(
                title=title,
                link=link,
                sort_no=sort_no,
                description=description,
                is_original=is_original,
                original_datetime=original_time,
                original_place=original_place
            )
        else:
            if source_link and source_name:
                photo = PhotoItem(
                    title=title,
                    link=link,
                    sort_no=sort_no,
                    description=description,
                    is_original=is_original,
                    source_name=source_name,
                    source_link=source_link
                )
            else:
                raise LogicException("非原创必须增加原链接和名称")

        photo.save()
        return Response({"created": photo.code})

    @cms_common
    @common_validate(required_fields=required_fields, type_fields=type_fields, logic_fields=logic_fields)
    def put(self, request):
        code = request.data.get("code", "")
        title = request.data.get("title")
        link = request.data.get("link")
        sort_no = request.data.get("sort_no")
        description = request.data.get("description")
        is_original = request.data.get("is_original")
        original_time = request.data.get("original_time")
        original_place = request.data.get("original_place")
        source_name = request.data.get("source_name")
        source_link = request.data.get("source_link")

        if is_original:
            try:
                original_time = datetime_str_fmt_utc8(original_time)
            except (ValueError, TypeError):
                raise LogicException("原创必须增加拍摄时间")
            updated = PhotoItem.objects.filter(open_code=code).update(
                title=title,
                link=link,
                sort_no=sort_no,
                description=description,
                is_original=is_original,
                original_datetime=original_time,
                original_place=original_place
            )
        else:
            if source_link and source_name:
                updated = PhotoItem.objects.filter(open_code=code).update(
                    title=title,
                    link=link,
                    sort_no=sort_no,
                    description=description,
                    is_original=is_original,
                    source_name=source_name,
                    source_link=source_link
                )
            else:
                raise LogicException("非原创必须增加原链接和名称")

        return Response({"updated": updated})

    @cms_common
    def delete(self, request):
        code = request.GET.get("code")
        deleted = PhotoItem.objects.filter(open_code=code).update(
            delete_flag=True,
            delete_time=timezone.now()
        )

        return Response({"deleted": deleted})


# 更新状态API字段校验
CMS_UPDATE_DISPLAY_STATUS_VALIDATE = {
    "required_fields": ['code', 'status'],
    "type_fields": {"status": int},
    "logic_fields": {"status": (lambda x: x in photowall_constant.PHOTO_SHOW_STATUS_LIST, '状态不存在')}
}

@api_view(["PUT"])
@permission_classes((CMSPhotoWallManager,))
@cms_common
@common_validate(**CMS_UPDATE_DISPLAY_STATUS_VALIDATE)
def cms_update_display_status(request):
    code = request.data.get("code")
    status = request.data.get("status")

    updated = PhotoItem.objects.filter(open_code=code).update(
        status=status
    )

    return Response({"updated": updated})


class CMSPreviewPhotoWall(APIView):

    permission_classes = (CMSPhotoWallManager,)

    @cms_common
    def get(self, request):
        query_set = PhotoItem.objects.all().order_by('sort_no')

        query_set_ser = CMSPreviewPhotoWallSerializers(query_set, many=True)

        # 暂时不给两种归类 因为前段自己会归类
        # usable_list = []
        # unusable_list = []
        # for r in query_set_ser.data:
        #     if r.get('status') == photowall_constant.PHOTO_SHOW_STATUS_DISPLAY:
        #         usable_list.append(r)
        #     else:
        #         unusable_list.append(r)
        #
        # data = {
        #     "usable_list": usable_list,
        #     "unusable_list": unusable_list
        # }

        return Response(data=query_set_ser.data)
