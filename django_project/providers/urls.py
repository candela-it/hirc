from django.conf.urls import patterns, url, include

from rest_framework.routers import DefaultRouter

from .views import ProviderResponseViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'providerresponses', ProviderResponseViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = patterns(
    '',
    url(r'^', include(router.urls)),
    # url(
    #     r'^api-auth/',
    #     include('rest_framework.urls', namespace='rest_framework')
    # )
)
