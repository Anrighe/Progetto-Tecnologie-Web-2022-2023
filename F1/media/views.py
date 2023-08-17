from datetime import date
from store.models import Utente
from media.forms import FormUtente
from django.shortcuts import render
from django.shortcuts import redirect
from media.models import News, Highlight
from django.views.generic.list import ListView
from django.core.paginator import Paginator, EmptyPage
from info.models import Partecipazione, Sessione, Circuito


class HomePageView(ListView):
    '''Gestisce la homepage del sito fornendo:
    * Le informazioni relative all'ultima sessione disputata 
    * Gli ultimi articoli pubblicati (fino a un massimo di 10) nel caso l'utente non sia loggato o non sia un utente regolare o sia un utente regolare che non segue nessuna scuderia
    * Gli ultimi articoli pubblicati dalle scuderie seguite (fino a un massimo di 5) dall'utente nel caso l'utente sia loggato e sia un utente regolare che segue almeno una scuderia più altri 5 articoli pubblicati dalle scuderie non seguite dall'utente
    * Lista dei gran premi passati apposta a quella dei gran premi futuri'''
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
        user = self.request.user

        if data_ultima_sessione:
            partecipazioni = Partecipazione.objects.filter(data=data_ultima_sessione).order_by('posizione')
            sessione = Sessione.objects.filter(partecipazione__in=partecipazioni).first()
            circuito = Circuito.objects.filter(partecipazione__in=partecipazioni).first()

            context['partecipazioni'] = partecipazioni
            context['tipo_sessione'] = sessione.tipo
            context['nome_circuito'] = circuito.nome
        
        utente_regolare = False
        gestore_circuito = False

        if user.is_authenticated:
            try:
                if user.utente:
                    utente_regolare = True
                    gestore_circuito = False
                    utente = Utente.objects.get(user=user)
            except:
                utente_regolare = False
                gestore_circuito = True

        if utente_regolare and utente.follow:
            news = News.objects.filter(tags__in=utente.follow.all()).order_by('-data')[:5]

            unfollowed_news = News.objects.exclude(tags__in=utente.follow.all()).order_by('-data')[:5]

            context['news'] = news
            context['unfollowed_news'] = unfollowed_news

        else:
            news = News.objects.filter().order_by('-data')[:10]
            context['news'] = news

        circuiti_futuri = Circuito.objects.filter(data_evento__gte=date.today()).order_by('data_evento')

        circuiti_passati = Circuito.objects.exclude(pk__in=circuiti_futuri).order_by('-data_evento')

        circuiti = [circuito for circuito in circuiti_futuri]
        [circuiti.append(circuito) for circuito in circuiti_passati]

        context['circuiti'] = circuiti
        context['data'] = date.today()

        return context
    
    
class HighlightPageView(ListView):
    '''Gestisce la pagina degli highlight, mostrando un massimo di 6 highlight per pagina, in ordine cronologico decrescente'''
    model = Highlight
    template_name = 'media/highlight.html' 
    NUM_VIDEO_PER_PAGINA = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        highlights = Highlight.objects.all().order_by('-data')
        paginator = Paginator(highlights, HighlightPageView.NUM_VIDEO_PER_PAGINA)
        
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
    '''Gestisce la pagina di un singolo highlight'''
    model = Highlight
    template_name = 'media/video_highlight.html'

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            pk = self.kwargs.get('pk')
            video = Highlight.objects.get(pk=pk)
            video.visualizzazioni += 1
            video.save()
            context['video'] = video
            return context
        except Highlight.DoesNotExist:
            return {}
        
    def get(self, request, *args, **kwargs):
        try:
            pk = self.kwargs.get('pk')
            video = Highlight.objects.get(pk=pk)
            return super().get(request, *args, **kwargs)
        except Exception:
            return redirect('nothing_here')
