from django.conf.urls import patterns, url

from .views import (
    Home,
    LogoutUser,
    delete_own_comment
)

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='homeview'),
    url(
        r'^comments/delete_own/(?P<id>.*)/$',
        delete_own_comment,
        name='delete_own_comment'
    ),
    url(r'^logout$', LogoutUser.as_view(), name='logout_user'),
)
