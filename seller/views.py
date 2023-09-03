from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from seller.forms import RegisterUserForm, LoginUserForm


def home(request):
    return render(request, 'seller/home.html')


def logout_user(request):
    logout(request)
    return redirect('login')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'seller/register.html'
    success_url = reverse_lazy('login')  # возвращаемся на форму в случае успеха


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'seller/login.html'

    def get_success_url(self):
        return reverse_lazy('login')  # возвращаемся на форму в случае успеха
