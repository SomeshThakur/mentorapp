from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from onlineapp.forms import *


class SignUpView(View):
    def get(self, request):
        signup_form = SignUpForm()
        return render(
            request,
            template_name="sign_up.html",
            context={'form': signup_form, 'title': 'Sign up'},
        )

    def post(self, request):
        sign_up = SignUpForm(request.POST)
        if sign_up.is_valid():
            if authenticate(username=sign_up.cleaned_data['username'],
                            password=sign_up.cleaned_data['password'], ):
                return HttpResponse("User Already Exits!")

            User.objects.create_user(**sign_up.cleaned_data)
            user = authenticate(
                request,
                username=sign_up.cleaned_data['username'],
                password=sign_up.cleaned_data['password'],
            )
            if user is not None:
                return redirect('colleges_list')


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()

        return render(
            request,
            template_name="login.html",
            context={'form': login_form, 'title': 'Login'},
        )

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(
                request,
                username=login_form.cleaned_data['username'],
                password=login_form.cleaned_data['password'],
            )
            if user:
                login(request, user)
                return redirect('colleges_list')
            else:
                return HttpResponse("Login Failed !")


def logout_user(request):
    logout(request)
    return redirect('login')
