import logging
logger = logging.getLogger(__name__)

from django.http import HttpResponse

from .models import Answer
from .forms import AnswerForm


from django.views.generic.edit import BaseUpdateView


class UpdateAnswer(BaseUpdateView):
    form_class = AnswerForm
    model = Answer

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        # Next, try looking up by primary key.
        req_id = self.kwargs.get('req_id', None)
        que_id = self.kwargs.get('que_id', None)
        queryset = queryset.filter(imagery_request=req_id, question=que_id)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except self.model.DoesNotExist:
            obj = self.model()
        return obj

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponse('ok')

    def form_invalid(self, form):
        resp = HttpResponse('Error processing Answer form')
        resp.status_code = 404
        return resp
