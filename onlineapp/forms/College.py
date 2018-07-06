from django import forms

from onlineapp.models import *

class CollegeForm(forms.ModelForm):
    class Meta:
        model = College
        exclude = ['id']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control','placeholder':'Enter College name'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter College Location'}),
            'acronym': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Acronym'}),
            'contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Contact Email'}),
        }