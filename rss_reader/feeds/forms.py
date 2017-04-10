from django import forms
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
import feedparser

from .models import Feed


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ('name', 'url')

    def __init__(self, *args, **kwargs):
        super(FeedForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.add_input(Submit('submit', 'add'))

    def clean_url(self):
        url = self.cleaned_data['url']

        if not feedparser.parse(url).version:
            raise forms.ValidationError(_('Probably invalid feed.'))

        return url
