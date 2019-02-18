# coding=utf-8

from rest_framework.response import Response
from rest_framework.decorators import api_view

from common.decorators import api_common

from photowall.models import PhotoItem
from photowall import constant as photo_wall_constant
from photowall.serializers.apis import PhotoWallListSerializers


@api_view(["GET"])
@api_common
def get_photo_wall_list(request):

    photo_items = PhotoItem.objects.filter(
        status=photo_wall_constant.PHOTO_SHOW_STATUS_DISPLAY
    ).order_by("sort_no")

    photo_items_ser = PhotoWallListSerializers(photo_items, many=True)

    return Response(data=photo_items_ser.data)
