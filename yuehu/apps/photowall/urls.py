# coding=utf-8

from django.urls import path

from photowall.apis import apis, cms


app_name = "photowall"

api_urlpatterns = [
    path('api/photo_wall_list/', apis.get_photo_wall_list, name='photo_wall_list'),
]

cms_urlpatterns = [
    path('cms/photo_manage/', cms.CMSManagePhotoWall.as_view(), name='cms_photo_manage'),
    path('cms/photo_change_display_status/', cms.cms_update_display_status, name='cms_photo_change_display_status'),
    path('cms/preview_photo_wall/', cms.CMSPreviewPhotoWall.as_view(), name='cms_preview_photo_wall'),
]

urlpatterns = api_urlpatterns + cms_urlpatterns
