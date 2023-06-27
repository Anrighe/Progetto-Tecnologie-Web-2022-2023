from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from store.models import Utente
from django.core.files.storage import FileSystemStorage
import os


@login_required
def UserProfile(request):
    user = request.user
    
    try:
        utente = Utente.objects.get(user=user)

        # Caricamento di una nuova immagine profilo
        if request.method == 'POST' and request.FILES['profile-image-file']:
            uploaded_file = request.FILES['profile-image-file']

            username = user.username
            
            path = os.path.join(os.getcwd(), 'static', 'users', username)

            # Cancella i file precedentemente presenti nella cartella dell'utente
            for file_name in os.listdir(path):
                file_path = os.path.join(path, file_name)
                if os.path.isfile(file_path):
                    os.remove(file_path)

            fs = FileSystemStorage(location=path)

            filename = fs.save(uploaded_file.name, uploaded_file)
            print("FILENAME", filename)

            utente.immagine_profilo = f'/static/users/{username}/{filename}'
            utente.save()

    except Utente.DoesNotExist:
        utente = None

    ctx = {'utente': utente}

    return render(request, 'store/user_profile.html', ctx)    