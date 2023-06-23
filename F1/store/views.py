from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from store.models import Utente




@login_required
def UserProfile(request):
    return render(request, 'store/user_profile.html')    
