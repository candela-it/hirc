import logging
logger = logging.getLogger(__name__)

from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib.comments.views.moderation import perform_delete
from django.contrib.comments.models import Comment
from django.http import Http404, HttpResponseRedirect


class Home(TemplateView):
    template_name = 'index.html'


class ListProjects(TemplateView):
    template_name = 'list_projects.html'


def delete_own_comment(request, id):
    """
    Adds delete own comment functionality.
    """
    comment = get_object_or_404(Comment, id=id)
    if comment.user.id != request.user.id:
        raise Http404
    perform_delete(request, comment)
    return HttpResponseRedirect(comment.content_object.get_absolute_url())
