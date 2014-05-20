import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.views.generic import DetailView
from django.contrib.auth import logout as auth_logout

from braces.views import JSONResponseMixin, LoginRequiredMixin

from imagery_requests.models import ImageryRequest, RequestStatus


class Home(TemplateView):
    template_name = 'index.html'


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
        result = {}
        statuses = RequestStatus.objects.all()
        for status in statuses:
            geometry = {}
            requests = ImageryRequest.objects.filter(status=status)
            for req in requests:
                geometry[req.id] = {
                    'id': req.id,
                    'title': req.title,
                    'polygon': req.area_of_interest.geojson
                }
            result[status.title] = geometry
        return self.render_json_response(result)
