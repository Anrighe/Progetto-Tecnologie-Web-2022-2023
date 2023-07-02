from django.urls import path
from store.views import UserProfile, UserProfileDataChangeView

app_name = 'store'

urlpatterns = [
    path('profile/', UserProfile, name='profile'),
    path('profile/modify/', UserProfileDataChangeView.as_view(), name='modify')
]
