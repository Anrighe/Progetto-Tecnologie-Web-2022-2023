from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from store.models import Utente


@login_required
def UserProfile(request):
    user = request.user
    
    try:
        utente = Utente.objects.get(user=user)
    except Utente.DoesNotExist:
        utente = None

    ctx = {'utente': utente}

    return render(request, 'store/user_profile.html', ctx)    