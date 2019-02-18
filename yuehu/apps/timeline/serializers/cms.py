# coding=utf-8

from collections import Iterable

from rest_framework import serializers

from timeline.models import TimelineLine, TimelineItem


class CMSTimeLineItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimelineItem
        fields = ["title", "date", "content", "code"]


class CMSAllTimeLineListSerializer(serializers.ModelSerializer):

    item_list = serializers.ListField()

    def __init__(self, instance, *args, **kwargs):

        if isinstance(instance, Iterable):
            for item in instance:
                item.item_list = CMSTimeLineItemSerializer(item.timeline_items.order_by("-date"), many=True).data
        else:
            instance.item_list = CMSTimeLineItemSerializer(instance.timeline_items.order_by("-date"), many=True).data
        super(CMSAllTimeLineListSerializer, self).__init__(instance, *args, **kwargs)

    class Meta:
        model = TimelineLine
        fields = ["year", "title", "content", "item_list", "code"]
