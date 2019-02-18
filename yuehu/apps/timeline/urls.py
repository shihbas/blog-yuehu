# coding=utf-8

from django.urls import path

from timeline.apis import apis,cms


app_name = "timeline"

api_urlpatterns = [
    path('api/timeline_list/', apis.APITimeLineList.as_view(), name='api_timeline_list'),
]

cms_urlpatterns = [
    path('cms/timeline/list/', cms.CMSTimeLine.as_view(), name='cms_timeline_list'),
    path('cms/timeline/item/', cms.CMSTimeLineItem.as_view(), name='cms_timeline_item'),
]

urlpatterns = api_urlpatterns + cms_urlpatterns
