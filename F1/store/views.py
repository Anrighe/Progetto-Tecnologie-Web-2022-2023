from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from store.models import Utente
from django.core.files.storage import FileSystemStorage
import os
from PIL import Image
from django.contrib import messages


@login_required
def UserProfile(request):
    ALLOWED_IMAGE_FORMATS = ['JPEG', 'JPG', 'PNG']
    user = request.user
    
    try:
        utente = Utente.objects.get(user=user)

        # Caricamento di una nuova immagine profilo
        if request.method == 'POST':
            uploaded_file = request.FILES.get('profile-image-file')
            
            # Se è stato effettivamente selezionato e caricato un file 
            if uploaded_file:
                image = Image.open(uploaded_file)

                if image.format in ALLOWED_IMAGE_FORMATS:

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
                else:
                    messages.error(request, 'Formato dell\'immagine non valido. Utilizza un file in formato JPEG, JPG, o PNG.')
            else:
                messages.error(request, 'Non è stata caricata nessuna immagine.')


    except Utente.DoesNotExist:
        utente = None

    ctx = {'utente': utente}

    return render(request, 'store/user_profile.html', ctx)    