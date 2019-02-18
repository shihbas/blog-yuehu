# coding=utf-8

from rest_framework import serializers

from banner.models import SlideShow


class SlideShowListSerializers(serializers.ModelSerializer):

    class Meta:
        model = SlideShow
        fields = ["sort_no", "title", "description", "img", "link", "date", "code"]
