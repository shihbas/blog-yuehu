# coding=utf-8

from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.decorators import api_common

from banner.models import SlideShow
from banner.serializers.apis import SlideShowListSerializers


@api_view(("GET",))
@api_common
def get_slide_show_list(request):

    slide_show_list_ser = SlideShowListSerializers(
        SlideShow.get_show_list(),
        many=True
    )
    return Response(data=slide_show_list_ser.data)
