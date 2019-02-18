# coding=utf-8

from rest_framework import serializers

from photowall.models import PhotoItem


class PhotoWallListSerializers(serializers.ModelSerializer):
    original_time = serializers.DateTimeField(source="original_datetime", format="%Y.%m.%d %H:%M", allow_null=True)

    class Meta:
        model = PhotoItem
        fields = ["title", "link", "description", "is_original", "code",
                  "source_name", "source_link",
                  "original_time", "original_place"]

