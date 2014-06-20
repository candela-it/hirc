from django.conf.urls import patterns, url

from .views import (
    AddRequest,
    EditRequest,
    AddRequestDate,
    DeleteRequestDate,
    EditRequestDate,
    ViewRequest,
    ListRequests,
    DownloadRequest,
)

urlpatterns = patterns(
    '',
    url(r'^requests/add$', AddRequest.as_view(), name='add_request'),
    url(
        r'^requests/add-date/(?P<pk>\d+)/$',
        AddRequestDate.as_view(),
        name='add_request_date'
    ),
    url(
        r'^requests/delete-date/(?P<pk>\d+)/$',
        DeleteRequestDate.as_view(),
        name='delete_request_date'
    ),
    url(
        r'^requests/edit-date/(?P<pk>\d+)/$',
        EditRequestDate.as_view(),
        name='edit_request_date'
    ),
    url(r'^requests/list$', ListRequests.as_view(), name='list_requests'),
    url(
        r'^requests/edit/(?P<pk>\d+)/$',
        EditRequest.as_view(),
        name='edit_request'
    ),
    url(
        r'^requests/(?P<pk>\d+)/$',
        ViewRequest.as_view(),
        name='view_request'
    ),
    url(r'^requests/download/(?P<pk>\d+)/$', DownloadRequest.as_view(),
        name='download_request')
)
