# coding=utf-8

from rest_framework import serializers

from account.models import UserDefaultAvatar


class ApiUserDefaultAvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserDefaultAvatar
        fields = ["avatar_url", "code"]
