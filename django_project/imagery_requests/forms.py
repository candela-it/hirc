import logging
logger = logging.getLogger(__name__)

import django.forms as forms

from .models import ImageryRequest


class ImageryRequestForm(forms.ModelForm):
    class Meta:
        model = ImageryRequest
        fields = ['title', 'description', 'area_of_interest']
        widgets = {
            'title': forms.TextInput(
                attrs={'placeholder': 'Enter project title'}),
            'description': forms.TextInput(
                attrs={'placeholder': 'Enter project description'}),
        }
