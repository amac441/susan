from django.forms import ModelForm, ChoiceField, CharField
from django import forms
from .models import Search
from django.core.validators import MinLengthValidator

class SearchForm(ModelForm):
    class Meta:
        model = Search
        exclude = ['from_user']

class LinkedinForm(forms.Form):
    search_for = forms.CharField(MinLengthValidator(1))

