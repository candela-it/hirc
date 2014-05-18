from django.conf.urls import patterns, url
from .views import Home, ListProjects, AddProject


urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='homeview'),
    url(r'^list$', ListProjects.as_view(), name='listprojects'),
    url(r'^project/add$', AddProject.as_view(), name='addproject'),
    # basic app views
    # url(r'^...', a_view)
)
