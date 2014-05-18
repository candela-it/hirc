from django.conf.urls import patterns, url
from .views import HomeView


urlpatterns = patterns(
    '',
    url(r'^$', HomeView.as_view(), name='homeview'),
    # basic app views
    # url(r'^...', a_view)
)
