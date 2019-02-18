# coding=utf-8

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from common.decorators import api_common

from timeline.models import TimelineLine
from timeline.serializers.apis import AllTimeLineListSerializer

class APITimeLineList(APIView):

    @api_common
    def get(self, request):

        timeline_set = TimelineLine.objects.prefetch_related("timeline_items").all().order_by("-year")

        timeline_ser = AllTimeLineListSerializer(timeline_set, many=True)

        return Response(data=timeline_ser.data)
