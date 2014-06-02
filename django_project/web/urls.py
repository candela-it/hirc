from django.conf.urls import patterns, url

from .views import (
    Home,
    LogoutUser,
    WorldGeoJson,
    RefreshComments,
    AboutPage
)

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='homeview'),
    url(r'^worldjson$', WorldGeoJson.as_view(), name='worldjson'),
    url(r'^about$', AboutPage.as_view(), name='about_page'),

    url(
        r'^refreshcomments/(?P<pk>\d+)$', RefreshComments.as_view(),
        name='refresh_comments'
    ),
    url(r'^logout$', LogoutUser.as_view(), name='logout_user'),
)
