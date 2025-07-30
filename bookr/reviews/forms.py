from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from .models import Publisher


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        max_length=200,
        min_length=3,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Search for a book', 'class': 'search-input'}))
    
    title = forms.BooleanField(required=False, label='Title')
    publisher = forms.BooleanField(required=False, label='Publisher')
    contributors = forms.BooleanField(required=False, label='Contributors')

    def clean(self):
        cleaned_data = super().clean()
        
        if not cleaned_data.get('title') and not cleaned_data.get('publisher') and not cleaned_data.get('contributors'):
            self.add_error(None, 'At least one field must be selected')