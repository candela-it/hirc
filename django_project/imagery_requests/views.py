import logging
logger = logging.getLogger(__name__)

from django.views.generic import (
    ListView,
    UpdateView,
    DetailView,
    CreateView,
    DeleteView
)
from django.views.generic.detail import BaseDetailView
from django import http

from braces.views import LoginRequiredMixin, JSONResponseMixin

from .forms import (
    ImageryRequestForm,
    ImageryRequestEditForm,
    RequestDateForm
)

from .models import ImageryRequest, RequestDate


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


class AddRequestDate(LoginRequiredMixin, JSONResponseMixin, CreateView):
    template_name = 'request_date_form.html'
    form_class = RequestDateForm
    model = RequestDate

    raise_exception = True

    def form_valid(self, form):
        self.object = form.save(commit=False)
        imagery_request = ImageryRequest.objects.get(pk=self.kwargs.get('pk'))
        self.object.imagery_request = imagery_request
        self.object.save()
        data = {'date': self.object.date,
                'time': self.object.time,
                'pk': self.object.pk}
        return self.render_json_response(data)

    def form_invalid(self, form):
        myResponse = self.render_to_response(self.get_context_data(form=form))
        myResponse.status_code = 404
        return myResponse


class EditRequestDate(LoginRequiredMixin, JSONResponseMixin, UpdateView):
    template_name = 'request_date_edit_form.html'
    form_class = RequestDateForm
    model = RequestDate
    pk_url_kwarg = 'pk'

    raise_exception = True

    def form_valid(self, form):
        self.object = form.save()
        data = {'date': self.object.date,
                'time': self.object.time,
                'pk': self.object.pk}
        return self.render_json_response(data)

    def form_invalid(self, form):
        myResponse = self.render_to_response(self.get_context_data(form=form))
        myResponse.status_code = 404
        return myResponse


class DeleteRequestDate(LoginRequiredMixin, DeleteView):
    model = RequestDate
    pk_url_kwarg = 'pk'

    raise_exception = True

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return http.HttpResponse('OK')


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
