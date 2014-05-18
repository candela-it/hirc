from django.conf.urls import patterns, url
from .views import Home, ListProjects


urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='homeview'),
    url(r'^list$', ListProjects.as_view(), name='listprojects'),
    # basic app views
    # url(r'^...', a_view)
)
