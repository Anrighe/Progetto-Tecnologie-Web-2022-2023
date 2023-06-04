from django.views.generic.list import ListView
from django.views.generic import DetailView
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
    
    def get_queryset(self):
        return self.model.objects.filter(titolo="Max Verstappen's Incredible Pole Lap | 2023 Monaco Grand Prix")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = Highlight.objects.all()
        context['query'] = query
        return context
    
class VideoHighlightPageView(ListView):
    model = Highlight
    template_name = 'media/video_highlight.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pk = self.kwargs.get('pk')
        video = Highlight.objects.get(pk=pk)
        video.visualizzazioni += 1
        video.save()
        context['video'] = video
        return context
