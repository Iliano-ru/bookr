from django import forms
from django.utils.safestring import mark_safe


class SearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        max_length=200,
        min_length=3,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Search for a book', 'class': 'search-input'}))