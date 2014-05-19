import logging
logger = logging.getLogger(__name__)

from django.shortcuts import get_object_or_404
from django.contrib.comments.views.moderation import perform_delete
from django.contrib.comments.models import Comment
from django.http import Http404, HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.contrib.auth import logout as auth_logout
from braces.views import JSONResponseMixin

from imagery_requests.models import ImageryRequest, RequestStatus


class Home(TemplateView):
    template_name = 'index.html'


def delete_own_comment(request, id):
    """
    Adds delete own comment functionality.
    """
    comment = get_object_or_404(Comment, id=id)
    if comment.user.id != request.user.id:
        raise Http404
    perform_delete(request, comment)
    return HttpResponseRedirect(comment.content_object.get_absolute_url())


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')


class WorldGeoJson(JSONResponseMixin, View):

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
