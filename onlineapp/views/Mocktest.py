from django.urls import reverse_lazy
from django.views.generic import CreateView

from onlineapp.forms import StudentForm
from onlineapp.models import Student


class CreateMocktestView(CreateView):
    model = Student
    form_class = StudentForm
    template_name = "mocktest_form.html"
    success_url = reverse_lazy('colleges_list')
