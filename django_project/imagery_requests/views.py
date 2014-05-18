import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, UpdateView, DetailView, CreateView

from .forms import ImageryRequestForm, ImageryRequestEditForm
from .models import ImageryRequest


class ListRequests(ListView):
    template_name = 'list_requests.html'
    context_object_name = 'requests'
    model = ImageryRequest


class AddRequest(CreateView):
    template_name = 'request_form.html'
    form_class = ImageryRequestForm
    model = ImageryRequest

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super(AddRequest, self).form_valid(form)


class EditRequest(UpdateView):
    template_name = 'request_form.html'
    form_class = ImageryRequestEditForm
    model = ImageryRequest


class ViewRequest(DetailView):
    context_object_name = 'request'
    model = ImageryRequest
    template_name = 'request_view.html'
