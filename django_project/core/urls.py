from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',

    # Enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^comments/', include('django_comments_xtd.urls')),
    # social-auth urls
    url('', include('social.apps.django_app.urls', namespace='social')),
    # web app urls
    url(r'', include('web.urls')),
    # Examples:
    # url(r'^hirc_app/', include('hirc_app.foo.urls')),
)
