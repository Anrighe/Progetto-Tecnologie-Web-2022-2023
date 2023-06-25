from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.core.paginator import Paginator, EmptyPage
from media.models import News, Highlight
from store.models import Utente
from info.models import Partecipazione, Sessione, Circuito
from media.forms import FormUtente
from django.shortcuts import redirect

from django.shortcuts import render

def crispy(request):
    context = {'form': FormUtente()}
    return render(request, 'media/crispy.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'media/homepage.html' 

    def trova_data_ultima_sessione():
        ultima_partecipazione = Partecipazione.objects.order_by('-data').first()

        if ultima_partecipazione:
            ultima_sessione = ultima_partecipazione.data
            return ultima_sessione
        else:
            return None
    
    def get_context_data(self):
        context = super().get_context_data()

        data_ultima_sessione = HomePageView.trova_data_ultima_sessione()

        if data_ultima_sessione:
            partecipazioni = Partecipazione.objects.filter(data=data_ultima_sessione).order_by('posizione')
            sessione = Sessione.objects.filter(partecipazione__in=partecipazioni).first()
            circuito = Circuito.objects.filter(partecipazione__in=partecipazioni).first()

            context['partecipazioni'] = partecipazioni
            context['tipo_sessione'] = sessione.tipo
            context['nome_circuito'] = circuito.nome

        # aggiungere [:n] con n = numero massimo di elementi da mostrare per ridurre le news caricate
        news = News.objects.filter().order_by('-data')
        context['news'] = news

        return context
    
    
class HighlightPageView(ListView):
    model = Highlight
    template_name = 'media/highlight.html' 
    NUM_VIDEO_PER_PAGINA = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        highlights = Highlight.objects.all().order_by('-data')
        paginator = Paginator(highlights, self.NUM_VIDEO_PER_PAGINA)
        
        numero_pagina = self.request.GET.get('page', 1)

        context['nothing_here'] = False

        pagina = paginator.page(numero_pagina)

        context['highlights'] = pagina
        context['num_pages'] = str(paginator.num_pages)

        return context
    
    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except EmptyPage:
            return redirect('nothing_here')
    

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
