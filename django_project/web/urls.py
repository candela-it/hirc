from django.conf.urls import patterns, url

from .views import (
    Home,
    LogoutUser
)

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='homeview'),

    url(r'^logout$', LogoutUser.as_view(), name='logout_user'),
)
