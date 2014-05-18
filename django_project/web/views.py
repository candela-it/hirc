import logging
logger = logging.getLogger(__name__)

from django.views.generic.base import TemplateView


class Home(TemplateView):
    template_name = 'index.html'


class ListProjects(TemplateView):
    template_name = 'list_projects.html'
