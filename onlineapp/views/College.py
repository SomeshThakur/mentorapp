from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import *
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from onlineapp.forms import CollegeForm
from onlineapp.models import *
from onlineapp.serializer import CollegeSerializer


class CollegeView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    # permission_denied_message = 'User does not have permissions'
    # raise_exception = True
    model = College
    context_object_name = "colleges_list"
    template_name = "colleges.html"

    def get_context_data(self, **kwargs):
        context = super(CollegeView, self).get_context_data(**kwargs)
        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
        })
        return context


class CollegeResults(LoginRequiredMixin, DetailView):
    login_url = '/login/'
    # permission_required = 'onlineapp.'
    # permission_denied_message = 'User does not have permissions'
    # raise_exception = True
    model = College
    template_name = "college_details.html"
    context_object_name = "students_list"

    def get_object(self, queryset=None):
        return get_object_or_404(College, **self.kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(CollegeResults, self).get_context_data(**kwargs)
        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
        })
        college = context.get('object')
        students = self.model.objects.filter(acronym=college.acronym).values('student__name', 'student__id',
                                                                             'student__college__acronym',
                                                                             'student__mocktest__totals').order_by(
            '-student__mocktest__totals')
        context.update({self.context_object_name: students})
        return context


class CreateCollegeView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = '/login/'
    permission_required = 'onlineapp.add_college'
    permission_denied_message = 'User does not have permissions'
    raise_exception = True
    model = College
    form_class = CollegeForm
    template_name = "college_form.html"
    success_url = reverse_lazy('colleges_list')

    def get_context_data(self, **kwargs):
        context = super(CreateCollegeView, self).get_context_data(**kwargs)
        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
        })
        return context


class EditCollegeView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = '/login/'
    permission_required = 'onlineapp.change_college'
    permission_denied_message = 'User does not have permissions'
    raise_exception = True
    model = College
    fields = [
        'name', 'acronym', 'location', 'contact'
    ]
    template_name = 'college_form.html'
    success_url = reverse_lazy('colleges_list')

    def get_context_data(self, **kwargs):
        context = super(EditCollegeView, self).get_context_data(**kwargs)
        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
        })
        return context


class DeleteCollegeView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    login_url = '/login/'
    permission_required = 'onlineapp.delete_college'
    permission_denied_message = 'User does not have permissions'
    raise_exception = True
    model = College
    template_name = "confirm_delete.html"
    success_url = reverse_lazy('colleges_list')

    def get_context_data(self, **kwargs):
        context = super(DeleteCollegeView, self).get_context_data(**kwargs)
        context.update({
            'user_permissions': self.request.user.get_all_permissions(),
        })
        return context


class CollegeApiAllView(APIView):
    def get(self, request):
        try:
            colleges = [CollegeSerializer(college).data for college in College.objects.all()]
        except:
            colleges = None
        return Response(colleges, status=200)

    def post(self, request):
        data = JSONParser().parse(request)
        serializer = CollegeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


class CollegeApiView(APIView):
    def get(self, request, **kwargs):
        try:
            college = College.objects.get(id=self.kwargs['pk'])
            college = CollegeSerializer(college).data
            return Response(college, status=200)
        except:
            return Response(data='No bro No College Found', status=404)

    def put(self, request, **kwargs):
        try:
            snippet = College.objects.get(pk=self.kwargs['pk'])
        except College.DoesNotExist:
            return HttpResponse(status=404)
        data = JSONParser().parse(request)
        serializer = CollegeSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request, **kwargs):
        try:
            snippet = College.objects.get(pk=self.kwargs['pk'])
        except College.DoesNotExist:
            return HttpResponse(status=404)
        snippet.delete()
        return HttpResponse(status=204)
