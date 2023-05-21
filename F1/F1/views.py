from django.shortcuts import render

def prova(request):
    return render(request,template_name="base.html")

