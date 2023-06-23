from django.urls import path
from store.views import UserProfile

app_name = 'store'

urlpatterns = [
    path('profile/', UserProfile, name='profile'),
]
