from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from seller.forms import RegisterUserForm, LoginUserForm


def home(request):
    context = {
        'title': "МАГАЗИН БУМАЖНЫХ МОДЕЛЕЙ:",
        'content': """ Вашему вниманию представлен сборник великолепных моделей из бумаги с инструкциями по сборке и лекала.<br>
        Модели разделены по категориям, рассчитаны на самый широкий круг увлеченных людей.<br>
        Создавайте прекрасные города, зоопарки, морские флотилии, аэродромы и железные дороги. Cами и вместе с детьми. """

    }
    return render(request, 'seller/home.html', context)


def contacts(request):
    context = {
        'title': "Контакты:",
        'content': """ Наш адрес: Москва, ул. Льва Толстого, дом 12 <br>
                    тел. +7-995-777-77-17, +7-995-777-77-16, +7-995-777-77-15<br>
                     e-mail: shop@paper-world.ru """

    }
    return render(request, 'seller/home.html', context)


def discounts(request):
    active_discount = [1, 2, 3]
    discount_info = ''
    for discount_inf in active_discount:
        discount_info += f"{discount_inf}<br>"
    context = {
        'title': "Информация о скидках:",
        'content': discount_info

    }
    return render(request, 'seller/home.html', context)


def logout_user(request):
    logout(request)
    return redirect('login')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'seller/register.html'
    success_url = reverse_lazy('goods')  # возвращаемся на форму в случае успеха


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'seller/login.html'

    def get_success_url(self):
        return reverse_lazy('goods')  # возвращаемся на форму в случае успеха
