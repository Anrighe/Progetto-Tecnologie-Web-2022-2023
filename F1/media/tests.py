from django.test import TestCase
from store.views import UtenteProfileDataChangeViewUpdate, StoreView
from media.views import HighlightPageView, VideoHighlightPageView
from django.contrib.auth.models import User, AnonymousUser
from store.models import Utente, TipologiaBiglietto, Gestore_Circuito
from info.models import Circuito
from django.test.client import Client
from django.test.utils import setup_test_environment
from django.urls import reverse
from media.models import Highlight
from django.urls.exceptions import NoReverseMatch


class HighlightTestCase(TestCase):
    def setUp(self):

        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.save()
        self.utente = Utente.objects.create(user=self.user)
        self.utente.save()

        self.highlight = []
        for i in range (1, 14):
            self.highlight.append(Highlight.objects.create(titolo='titolo '+str(i), preview='immagine '+str(i), video='video '+str(i), data='2023-09-09', visualizzazioni=10, portale_f1=None))
            self.highlight[0].save()

        self.client = Client()

    def test_first_highlight_found(self):
        self.reverse_highlight = reverse('media:highlight_video', kwargs={'pk': 1})
        
        self.response = self.client.get(self.reverse_highlight)
        self.assertEqual(self.response.status_code, 200)

    def test_last_highlight_found(self):
        self.reverse_highlight = reverse('media:highlight_video', kwargs={'pk': 13})
        
        self.response = self.client.get(self.reverse_highlight)
        self.assertEqual(self.response.status_code, 200)

    def test_highlight_not_found(self):
        self.reverse_highlight = reverse('media:highlight_video', kwargs={'pk': 100})

        self.response = self.client.get(self.reverse_highlight)
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.response.url, '/nothing_here/')
    
    def test_highlight_string_numbers_found(self):
        self.reverse_highlight = reverse('media:highlight_video', kwargs={'pk': '5'})

        self.response = self.client.get(self.reverse_highlight)
        self.assertEqual(self.response.status_code, 200)

    def test_highlight_string_numbers_not_found(self):
        self.reverse_highlight = reverse('media:highlight_video', kwargs={'pk': '50000'})

        self.response = self.client.get(self.reverse_highlight)
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.response.url, '/nothing_here/')

    def test_highlight_negative_not_found(self):
        self.reverse_highlight = reverse('media:highlight_video', kwargs={'pk': -1})

        self.response = self.client.get(self.reverse_highlight)
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.response.url, '/nothing_here/')

    def test_highlight_string_not_found(self):
        self.reverse_highlight = reverse('media:highlight_video', kwargs={'pk': 'ciao#*§°&%'})

        self.response = self.client.get(self.reverse_highlight)
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.response.url, '/nothing_here/')


    def test_highlight_generic_view_no_page(self):
        self.reverse_highlight = reverse('media:highlight')

        self.response = self.client.get(self.reverse_highlight)
        self.assertEqual(self.response.status_code, 200)

    def test_highlight_generic_view_page_found(self):
        self.reverse_highlight = reverse('media:highlight') + '?page=2'

        self.response = self.client.get(self.reverse_highlight)
        self.assertEqual(self.response.status_code, 200)
            
    def test_highlight_generic_view_page_not_found(self):
        self.reverse_highlight = reverse('media:highlight') + '?page=2000'

        self.response = self.client.get(self.reverse_highlight)
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.response.url, '/nothing_here/')


    def tearDown(self):
        self.user.delete()
        self.utente.delete()

        for highlight in self.highlight:
            highlight.delete()