import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, View
from django.views.generic import FormView, ListView
from django.contrib.auth import logout as auth_logout

from imagery_requests.forms import ImageryRequestForm
from imagery_requests.models import ImageryRequest


class Home(TemplateView):
    template_name = 'index.html'


class ListProjects(ListView):
    template_name = 'list_projects.html'
    context_object_name = 'projects'
    model = ImageryRequest


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')


class AddProject(FormView):
    template_name = 'project_form.html'
    form_class = ImageryRequestForm
