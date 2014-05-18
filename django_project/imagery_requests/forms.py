import logging
logger = logging.getLogger(__name__)

import django.forms as forms

from .models import ImageryRequest


class ImageryRequestForm(forms.ModelForm):
    class Meta:
        model = ImageryRequest
        fields = ['title', 'description', 'area_of_interest', 'question_set']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter project title'}),
            'description': forms.TextInput(
                attrs={'placeholder': 'Enter project description'}),
            'question_set': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super(ImageryRequestForm, self).__init__(*args, **kwargs)
        self.fields['question_set'].empty_label = None
        # following line needed to refresh widget copy of choice list
        self.fields['question_set'].widget.choices = (
            self.fields['question_set'].choices)


class ImageryRequestFormEdit(forms.ModelForm):
    class Meta:
        model = ImageryRequest
        fields = [
            'title',
            'description',
            'area_of_interest',
            'question_set',
            'status'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter project title'}),
            'description': forms.TextInput(
                attrs={'placeholder': 'Enter project description'}),
            'question_set': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super(ImageryRequestForm, self).__init__(*args, **kwargs)
        self.fields['question_set'].empty_label = None
        # following line needed to refresh widget copy of choice list
        self.fields['question_set'].widget.choices = (
            self.fields['question_set'].choices)
