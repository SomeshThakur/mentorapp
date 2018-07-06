from django import forms

from onlineapp.models import *


class MocktestForm(forms.ModelForm):
    class Meta:
        model = Mocktest
        exclude = ['id', 'student', 'totals']
        widgets = {
            'problem1': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Enter marks'}),
            'problem2': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Enter marks'}),
            'problem3': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Enter marks'}),
            'problem4': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'placeholder': 'Enter marks'}),
        }
