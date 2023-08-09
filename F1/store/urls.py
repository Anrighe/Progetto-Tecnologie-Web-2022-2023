from django.urls import path
from store.views import UserProfile, UtenteProfileDataChangeViewUpdate, StoreView, ProductView, CartView, GestoreProfileDataChangeViewUpdate, CreateTicketTypeView, CreateTicketInstanceView

app_name = 'store'

urlpatterns = [
    path('profile/', UserProfile, name='profile'),
    path('profile/modify_utente/<int:pk>/', UtenteProfileDataChangeViewUpdate.as_view(), name='modify_utente_update'),
    path('profile/modify_gestore/<int:pk>/', GestoreProfileDataChangeViewUpdate.as_view(), name='modify_gestore_update'),
    path('profile/create_ticket_type/', CreateTicketTypeView.as_view(), name='create_ticket_type'),
    path('profile/create_ticket_instance/', CreateTicketInstanceView.as_view(), name='create_ticket_instance'),
    path('store/', StoreView.as_view(), name='store'),
    path('store/product/<int:pk>/', ProductView.as_view(), name='product'),
    path('cart/', CartView.as_view(), name='cart'),
]
