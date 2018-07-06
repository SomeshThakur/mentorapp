from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, DeleteView, UpdateView
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from onlineapp.forms import *
from onlineapp.models import *
from onlineapp.serializer import StudentDetailsSerializer


class DeleteStudentView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = '/login/'
    permission_denied_message = 'User does not have permissions'
    raise_exception = True
    model = Student
    template_name = "confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super(DeleteStudentView, self).get_context_data(**kwargs)
        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
        })
        return context

    def post(self, request, *args, **kwargs):
        student = self.model.objects.get(id=kwargs['pk'])
        student.delete()
        return redirect('college_details', kwargs['acronym'])


class EditStudentView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    permission_denied_message = 'User does not have permissions'
    raise_exception = True
    model = Student
    template_name = "student_form.html"
    form_class = StudentForm

    def get_context_data(self, **kwargs):
        context = super(EditStudentView, self).get_context_data(**kwargs)
        student_form = context.get('form')
        student = context['object']
        mocktest_form = MocktestForm(instance=Mocktest.objects.get(student=student))
        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
        })
        context.update({
            'student': student_form,
            'mock': mocktest_form,
        })
        return context

    def post(self, request, *args, **kwargs):
        # ipdb.set_trace()
        acr = kwargs['acronym']
        college_object = College.objects.get(acronym=acr)
        try:
            mocktest = get_object_or_404(Mocktest, student_id=self.kwargs.get('pk'))
        except:
            mocktest = None

        student = Student.objects.get(id=self.kwargs.get('pk'))
        student_form = StudentForm(request.POST, instance=student)
        mock_form = MocktestForm(request.POST, instance=mocktest)
        if student_form.is_valid():
            student.save()
            if mock_form.is_valid():
                mocktest.totals = sum(mock_form.cleaned_data.values())
                mocktest.save()
        return redirect("college_details", college_object.acronym)


class CreateStudentView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/login/'
    permission_denied_message = 'User does not have permissions'
    raise_exception = True
    model = Student
    form_class = StudentForm
    template_name = "student_form.html"

    def get_context_data(self, **kwargs):
        context = super(CreateStudentView, self).get_context_data(**kwargs)
        student_form = context.get('form')
        mocktest_form = MocktestForm()

        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
        })

        context.update({
            'student': student_form,
            'mock': mocktest_form,
        })
        return context

    def post(self, request, *args, **kwargs):
        college = get_object_or_404(College, **kwargs)
        student_form = StudentForm(request.POST)
        mocktest_form = MocktestForm(request.POST)

        if student_form.is_valid():
            student = student_form.save(commit=False)
            student.college = college
            student.save()

            if mocktest_form.is_valid():
                mocktest = mocktest_form.save(commit=False)
                mocktest.totals = sum(mocktest_form.cleaned_data.values())
                mocktest.student = student
                mocktest.save()
            return redirect('college_details', college.acronym)


class StudentDetailsApiView(APIView):

    def get(self, request, **kwargs):
        status = 0
        try:
            if 'spk' in kwargs.keys() and 'pk' in kwargs.keys():
                college = College.objects.get(id=self.kwargs['pk'])
                students = StudentDetailsSerializer(Student.objects.filter(college=college).get(id=kwargs['spk'])).data
                status = 200
            elif 'pk' in kwargs.keys():
                college = College.objects.get(id=kwargs['pk'])
                students = [StudentDetailsSerializer(student).data for student in
                            Student.objects.filter(college=college)]
                status = 200
            else:
                students = [StudentDetailsSerializer(student).data for student in
                            Student.objects.all()]
                status = 200
        except:
            status = 404
            students = None
        return Response(students, status=status)

    def post(self, request, **kwargs):
        if 'pk' in kwargs.keys():
            college = College.objects.get(id=self.kwargs['pk'])
            data = JSONParser().parse(request)
            ser = StudentDetailsSerializer(data=data)
            if ser.is_valid():
                student = ser.save(college=college)
                student.save()
                return Response(ser.data, status=201)
            return Response(ser.errors, status=400)

    def put(self, request, **kwargs):
        try:
            if 'spk' in kwargs.keys() and 'pk' in kwargs.keys():
                student = Student.objects.get(id=kwargs['spk'])
                data = JSONParser().parse(request)
                ser = StudentDetailsSerializer(student, data=data)
                if ser.is_valid():
                    ser.save()
                    return Response(ser.data, status=201)
                return Response(ser.errors, status=400)
        except:
            return Response(status=404)

    def delete(self, request, **kwargs):
        try:
            if 'spk' in kwargs.keys() and 'pk' in kwargs.keys():
                student = Student.objects.get(id=kwargs['spk'])
                student.delete()
        except ObjectDoesNotExist:
            return HttpResponse(status=404)
        return HttpResponse(status=204)
