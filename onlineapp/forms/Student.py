from django import forms

from onlineapp.models import *


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['id', 'dob', 'college']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter College name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'db_folder': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Db name Email'}),
            'dropped_out': forms.CheckboxInput(),
        }
