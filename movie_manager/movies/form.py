from django import forms
from django.forms import ModelForm
from . models import movieinfo

class movieForm(ModelForm):
    class Meta:
        model=movieinfo
        fields='__all__'
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'year': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded px-3 py-2',
                'rows': 4 
            }),
        }