# coding=utf-8

from collections import Iterable

from rest_framework import serializers

from django.contrib.auth.models import Permission, Group

from account.models import User


class CMSPermissionDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["name", "codename"]


class CMSGroupListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ["name"]


class CMSGroupDetailSerializer(serializers.ModelSerializer):

    permission_list = serializers.ListField()

    def __init__(self, instance, *args, **kwargs):
        if isinstance(instance, Iterable):
            for item in instance:
                item.permission_list = CMSPermissionDetailSerializer(item.permissions.all(), many=True).data
        else:
            instance.permission_list = CMSPermissionDetailSerializer(instance.permissions.all(), many=True).data
        super(CMSGroupDetailSerializer, self).__init__(instance, *args, **kwargs)

    class Meta:
        model = Group
        fields = ["name", "permission_list"]


class CMSAccountListForGroup(serializers.ModelSerializer):
    group_list = serializers.ListField()
    join_datetime = serializers.DateTimeField(source="date_joined", format="%Y.%m.%d %H:%M")

    def __init__(self, instance, *args, **kwargs):
        if isinstance(instance, Iterable):
            for item in instance:
                item.group_list = CMSGroupListSerializer(item.groups.all(), many=True).data
        else:
            instance.group_list = CMSGroupListSerializer(instance.groups.all(), many=True).data

        super(CMSAccountListForGroup, self).__init__(instance, *args, **kwargs)

    class Meta:
        model = User
        fields = ["display_name", "display_phone", "display_email", "open_id", "join_datetime", "group_list"]


class CMSAccountDetailForGroup(serializers.ModelSerializer):
    join_datetime = serializers.DateTimeField(source="date_joined", format="%Y.%m.%d %H:%M")

    class Meta:
        model = User
        fields = ["display_name", "display_phone", "display_email", "open_id", "join_datetime", "is_cms"]
