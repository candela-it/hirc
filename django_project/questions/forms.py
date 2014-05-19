import logging
logger = logging.getLogger(__name__)

import django.forms as forms

from .models import Answer


class AnswerForm(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['text', 'imagery_request', 'question']
        widgets = {
            'imagery_request': forms.HiddenInput(),
            'question': forms.HiddenInput()
        }

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)
