# coding=utf-8

from collections import Iterable

from rest_framework import serializers

from timeline.models import TimelineLine, TimelineItem


class TimeLineItemSerializer(serializers.ModelSerializer):
    date_str = serializers.DateField(source="date", format="%m月%d日")

    class Meta:
        model = TimelineItem
        fields = ["title", "date_str", "content", "code"]


class AllTimeLineListSerializer(serializers.ModelSerializer):

    item_list = serializers.ListField()

    def __init__(self, instance, *args, **kwargs):

        if isinstance(instance, Iterable):
            for item in instance:
                item.item_list = TimeLineItemSerializer(item.timeline_items.order_by("-date"), many=True).data
        else:
            instance.item_list = TimeLineItemSerializer(instance.timeline_items.order_by("-date"), many=True).data
        super(AllTimeLineListSerializer, self).__init__(instance, *args, **kwargs)

    class Meta:
        model = TimelineLine
        fields = ["year", "title", "content", "item_list", "code"]
