import logging
logger = logging.getLogger(__name__)

from django.views.generic.base import TemplateView
from django.views.generic import FormView

from imagery_requests.forms import ImageryRequestForm


class Home(TemplateView):
    template_name = 'index.html'


class ListProjects(TemplateView):
    template_name = 'list_projects.html'


class AddProject(FormView):
    template_name = 'project_form.html'
    form_class = ImageryRequestForm
