from django.conf.urls import patterns, url

from .views import (
    Home,
    ListProjects,
    LogoutUser,
    AddProject,
    EditProject,
    ViewProject
)

urlpatterns = patterns(
    '',
    url(r'^$', Home.as_view(), name='homeview'),
    url(r'^list$', ListProjects.as_view(), name='listprojects'),
    url(r'^project/add$', AddProject.as_view(), name='addproject'),
    url(
        r'^project/edit/(?P<pk>\d+)/$',
        EditProject.as_view(),
        name='editproject'
    ),
    url(
        r'^project/(?P<pk>\d+)/$',
        ViewProject.as_view(),
        name='viewproject'
    ),

    url(r'^logout$', LogoutUser.as_view(), name='logout_user'),
)
