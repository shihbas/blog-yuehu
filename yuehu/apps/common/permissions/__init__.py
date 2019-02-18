# coding=utf-8

from rest_framework.permissions import BasePermission


class IsNotLogin(BasePermission):

    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsLogin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated
