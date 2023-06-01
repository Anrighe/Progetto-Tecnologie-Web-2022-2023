from django.views.generic.list import ListView
from info.models import Circuito

from media.forms import FormUtente

from django.shortcuts import get_object_or_404, render

def crispy(request):
    context = {'form': FormUtente()}
    return render(request, 'media/crispy.html', context)


def monaco_view(request):
    ctx = {"obj": get_object_or_404(Circuito, nome='MONACO')}
    return render(request, template_name='info/circuito.html', context=ctx)