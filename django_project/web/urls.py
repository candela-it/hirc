from django.conf.urls import patterns, url
from .views import Home, ListProjects, delete_own_comment


urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='homeview'),
    url(r'^list$', ListProjects.as_view(), name='listprojects'),
    url(
        r'^comments/delete_own/(?P<id>.*)/$',
        delete_own_comment,
        name='delete_own_comment'
    ),
    # basic app views
    # url(r'^...', a_view)
)
