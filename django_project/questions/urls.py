from django.conf.urls import patterns, url

from .views import UpdateAnswer

urlpatterns = patterns(
    '',
    url(
        r'^answer/add/(?P<req_id>\d+)/(?P<que_id>\d+)$',
        UpdateAnswer.as_view(), name='add_answer'
    )
)
