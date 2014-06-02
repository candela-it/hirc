import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.views.generic import DetailView
from django.contrib.auth import logout as auth_logout

from braces.views import JSONResponseMixin, LoginRequiredMixin

from imagery_requests.models import ImageryRequest


class Home(TemplateView):
    template_name = 'index.html'


class AboutPage(TemplateView):
    template_name = 'about.html'


class RefreshComments(LoginRequiredMixin, DetailView):

    raise_exception = True

    context_object_name = 'request'
    model = ImageryRequest
    template_name = 'request_comments.html'


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')


class WorldGeoJson(LoginRequiredMixin, JSONResponseMixin, View):

    raise_exception = True

    def get(self, request, *args, **kwargs):
        requests = ImageryRequest.objects.all().select_related()
        return self.render_json_response([
            req.as_geojson() for req in requests
        ])
