import logging
logger = logging.getLogger(__name__)

from django.views.generic import FormView, ListView, UpdateView, DetailView

from .forms import ImageryRequestForm, ImageryRequestEditForm
from .models import ImageryRequest


class ListRequests(ListView):
    template_name = 'list_requests.html'
    context_object_name = 'requests'
    model = ImageryRequest


class AddRequest(FormView):
    template_name = 'request_form.html'
    form_class = ImageryRequestForm

    def form_valid(self, form):
        pass


class EditRequest(UpdateView):
    template_name = 'request_form'
    form_class = ImageryRequestEditForm


class ViewRequest(DetailView):
    context_object_name = 'request'
    model = ImageryRequest
    template_name = 'request_view.html'
