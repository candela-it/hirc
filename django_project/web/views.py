import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponseRedirect
from django.views.generic.base import TemplateView, View

from django.contrib.auth import logout as auth_logout


class Home(TemplateView):
    template_name = 'index.html'


class LogoutUser(View):
    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return HttpResponseRedirect('/')
