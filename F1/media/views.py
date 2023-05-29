from django.views.generic.list import ListView
from media.models import News, Highlight
from store.models import Utente

from media.forms import FormUtente

from django.shortcuts import render

def crispy(request):
    context = {'form': FormUtente()}
    return render(request, 'media/crispy.html', context)

class HomePageView(ListView):
    model = News
    template_name = 'media/homepage.html' 

    #def get_queryset(self):
        #return self.model.objects.exclude(autore='Enrico')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo'] = 'News'

        form = FormUtente()

        query_utenti = Utente.objects.all()
        context['query_utenti'] = query_utenti
        context['form'] = form
        return context
    
class HighlightPageView(ListView):
    model = Highlight
    template_name = 'media/highlight.html' 
    
    


