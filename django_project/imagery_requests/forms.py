import logging
logger = logging.getLogger(__name__)

import django.forms as forms

from .models import ImageryRequest, RequestDate


class ImageryRequestForm(forms.ModelForm):
    area_of_interest = forms.CharField(
        widget=forms.Textarea({'hidden': ''}),
        error_messages={'required': 'Please select an area of interest.'}
    )

    class Meta:
        model = ImageryRequest
        fields = ['title', 'description', 'area_of_interest', 'question_set']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter a request title'}),
            'description': forms.TextInput(
                attrs={'placeholder': 'Enter a request description'}),
            'question_set': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs):
        super(ImageryRequestForm, self).__init__(*args, **kwargs)
        self.fields['question_set'].empty_label = None
        # following line needed to refresh widget copy of choice list
        self.fields['question_set'].widget.choices = (
            self.fields['question_set'].choices
        )
        self.fields['question_set'].error_messages = (
            {'required': 'Please select a question set.'}
        )


class ImageryRequestEditForm(forms.ModelForm):
    area_of_interest = forms.CharField(widget=forms.Textarea({'hidden': ''}))

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
                attrs={'placeholder': 'Enter request title'}
            ),
            'description': forms.TextInput(
                attrs={'placeholder': 'Enter request description'}
            ),
            'question_set': forms.RadioSelect(),
            'status': forms.RadioSelect()
        }

    def __init__(self, *args, **kwargs):
        super(ImageryRequestEditForm, self).__init__(*args, **kwargs)
        self.fields['question_set'].empty_label = None
        # following line needed to refresh widget copy of choice list
        self.fields['question_set'].widget.choices = (
            self.fields['question_set'].choices
        )


class RequestDateForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(format='%d/%m/%Y'),
        input_formats=('%d/%m/%Y',))

    class Meta:
        model = RequestDate
        fields = ['date', 'time']
