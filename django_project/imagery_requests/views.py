import logging
logger = logging.getLogger(__name__)

from django.views.generic import ListView, UpdateView, DetailView, CreateView
from django.views.generic.detail import BaseDetailView
from django import http

from braces.views import LoginRequiredMixin

from .forms import ImageryRequestForm, ImageryRequestEditForm
from .models import ImageryRequest


class ListRequests(LoginRequiredMixin, ListView):
    template_name = 'list_requests.html'
    context_object_name = 'requests'
    model = ImageryRequest


class AddRequest(LoginRequiredMixin, CreateView):
    template_name = 'request_form.html'
    form_class = ImageryRequestForm
    model = ImageryRequest

    raise_exception = True

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.created_by = self.request.user
        self.object.save()
        return super(AddRequest, self).form_valid(form)


class EditRequest(LoginRequiredMixin, UpdateView):
    template_name = 'request_form.html'
    form_class = ImageryRequestEditForm
    model = ImageryRequest

    raise_exception = True


class ViewRequest(LoginRequiredMixin, DetailView):
    context_object_name = 'request'
    model = ImageryRequest
    template_name = 'request_view.html'


class DownloadRequest(LoginRequiredMixin, BaseDetailView):
    model = ImageryRequest

    raise_exception = True

    def render_to_response(self, context):
        request = context['object']

        return self.json_response(
            content=request.area_of_interest.geojson,
            filename=request.title
        )

    def json_response(self, content, filename, **httpresponse_kwargs):
        response = http.HttpResponse(
            content, content_type='application/json', **httpresponse_kwargs
        )

        response['Content-Disposition'] = '{}; filename="{}.geojson"'.format(
            'attachment', filename)

        return response
