import logging
logger = logging.getLogger(__name__)

from django import forms
from django.contrib.comments.forms import CommentForm
from django_comments_xtd.conf import settings
from django_comments_xtd.models import TmpXtdComment


class CustomXtdCommentForm(CommentForm):
    followup = forms.BooleanField(
        required=False, label="Notify me of follow up comments via email"
    )
    reply_to = forms.IntegerField(
        required=True, initial=0, widget=forms.HiddenInput()
    )

    def __init__(self, *args, **kwargs):
        comment = kwargs.pop("comment", None)
        if comment:
            initial = kwargs.pop("initial", {})
            initial.update({"reply_to": comment.pk})
            kwargs["initial"] = initial
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['name'] = forms.CharField(
            widget=forms.TextInput(attrs={'placeholder': 'name'}))
        self.fields['comment'] = forms.CharField(
            widget=forms.Textarea(attrs={'placeholder': 'comment'}),
            max_length=settings.COMMENT_MAX_LENGTH)
        # make email optional
        self.fields['email'].required = False

    def get_comment_model(self):
        return TmpXtdComment

    def get_comment_create_data(self):
        data = super(CommentForm, self).get_comment_create_data()
        data.update({'thread_id': 0, 'level': 0, 'order': 1,
                     'parent_id': self.cleaned_data['reply_to'],
                     'followup': self.cleaned_data['followup']})
        if settings.COMMENTS_XTD_CONFIRM_EMAIL:
            # comment must be verified before getting approved
            data['is_public'] = False
        return data
