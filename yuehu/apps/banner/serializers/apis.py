# coding=utf-8

from rest_framework import serializers

from banner.models import SlideShow


class SlideShowListSerializers(serializers.ModelSerializer):

    created = serializers.DateField(source="date", format="%Y/%m/%d")

    class Meta:

        model = SlideShow
        fields = ["title", "description", "display_img", "link", "created"]
