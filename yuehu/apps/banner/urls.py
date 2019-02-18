# coding=utf-8

from django.conf.urls import url

from banner.apis import apis, cms

app_name = "banner"

api_urlpatterns = [
    url("^api/slice_show_list/$", apis.get_slide_show_list, name="get_slide_show_list"),
]

cms_urlpatterns = [
    url("^cms/manage_slice_show/$", cms.CMSManageSlideShow.as_view(), name="cms_manage_slice_show"),
]

urlpatterns = api_urlpatterns + cms_urlpatterns
