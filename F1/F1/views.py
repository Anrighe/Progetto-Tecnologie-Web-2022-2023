from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.shortcuts import render
from django.urls import reverse_lazy
from store.models import Utente
from media.models import PortaleF1

def prova(request):
    return render(request,template_name='base.html')


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/user_create.html'
    success_url = reverse_lazy('media:homepage')

    def form_valid(self, form):
        # Salva il model dell'istanza dell'User
        response = super().form_valid(form)

        portale_f1 = PortaleF1.objects.first()

        # Crea un'istanza di Utente e la connette al suo corrispettivo "User" e al "PortaleF1"
        Utente.objects.create(user=self.object, portale_f1=portale_f1)

        return response
    

def nothing_here(request):
    return render(request, template_name='nothing_here.html')

    