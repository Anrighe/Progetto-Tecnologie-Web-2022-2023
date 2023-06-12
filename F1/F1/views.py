from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy


def prova(request):
    return render(request,template_name='base.html')


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'store/user_create.html'
    success_url = reverse_lazy('media:homepage')